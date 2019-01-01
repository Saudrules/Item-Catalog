#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item
from sqlalchemy.pool import SingletonThreadPool
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db?check_same_thread=False',
                       poolclass=SingletonThreadPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Item catalog App'


# Create anti-forgery state token

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase
                    + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():

    # Only disconnect a connected user.

    access_token = login_session.get('access_token')
    if access_token is None:
        response = \
            make_response(json.dumps('Current user not connected.'),
                          401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.
                                 dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        del login_session['gplus_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        return redirect('/')
    else:
        response = \
            make_response(json.
                          dumps('Failed to revoke token for given user.',
                                400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON Endpoiunt for the whole catalog (Without items).

@app.route('/catalog/JSON')
def catalogJSON():
    catalog = session.query(Category).distinct().all()
    return jsonify(categories=[c.serialize for c in catalog])


# JSON Endpoint for all items in a given category.

@app.route('/catalog/<int:category_id>/JSON')
def categoryJSON(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[i.serialize for i in items])


# JSON Endpoint for an arbitrary item in the catalog.

@app.route('/catalog/items/<int:item_id>/JSON')
def itemJSON(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    catalog = session.query(Category).all()
    allItems = session.query(Item).all()
    if 'username' not in login_session:
        return render_template('catalog.html', catalog=catalog,
                               login_session=login_session)
    return render_template('catalog2.html', catalog=catalog,
                           login_session=login_session)


@app.route('/catalog/<int:category_id>', methods=['POST', 'GET'])
def showCategory(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    thisCategory = \
        session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return render_template('category.html', items=items,
                               thisCategory=thisCategory,
                               category_id=category_id,
                               login_session=login_session)
    return render_template('category2.html', items=items,
                           thisCategory=thisCategory,
                           category_id=category_id,
                           login_session=login_session)


@app.route('/catalog/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id,
                                         category_id=category_id).one()
    if 'username' not in login_session:
        return render_template('itemNA.html', item=item,
                               item_id=item_id, category_id=category_id,
                               login_session=login_session)
    return render_template('item.html', item=item, item_id=item_id,
                           category_id=category_id,
                           login_session=login_session)


@app.route('/catalog/add', methods=['POST', 'GET'])
def addItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        c = request.form['category']
        cat = session.query(Category).filter_by(name=c).one()
        newItem = Item(name=request.form['name'],
                       description=request.form['desc'],
                       category_id=cat.id,
                       user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New item %s successfully added in category %s .'
              % (newItem.name, cat.name))
        return redirect(url_for('showCatalog'))
    else:
        return render_template('addItem.html',
                               login_session=login_session)


@app.route('/catalog/<int:category_id>/<int:item_id>/edit',
           methods=['POST', 'GET'])
def editItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id,
                                         category_id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != item.user_id:
        return "<script>function myFunction() {alert('You are not \
        authorized to edit this item.'\
        );}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        c = request.form['category']
        cat = session.query(Category).filter_by(name=c).one()
        if request.form['name']:
            item.name = request.form['name']
        if request.form['desc']:
            item.description = request.form['desc']
        if request.form['category']:
            item.category_id = cat.id
            editedItem = item
        session.delete(item)
        session.add(editedItem)
        session.commit()
        flash('Item %s has been successfully edited.' % item.name)
        return redirect(url_for('showCategory',
                        category_id=category_id))
    else:
        return render_template('editItem.html', item=item, item_id=item_id,
                               category_id=category_id,
                               login_session=login_session)


@app.route('/catalog/<int:category_id>/<int:item_id>/delete',
           methods=['POST', 'GET'])
def deleteItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id,
                                         category_id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != item.user_id:
        return "<script>function myFunction() {alert('You are not \
        authorized to delete this item.'\
        );}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item %s has been successfully deleted.' % item.name)
        return redirect(url_for('showCategory',
                        category_id=category_id))
    else:
        return render_template('deleteItem.html', item=item,
                               item_id=item_id, category_id=category_id,
                               login_session=login_session)


if __name__ == '__main__':
    app.secret_key = 'super_secure'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
