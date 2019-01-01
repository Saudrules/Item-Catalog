# HERE WE START FILLING THE DATABASE WITH DATA
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Base, Category, Item


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


# Creating user
user1 = User(name="Saud otb", email="entertainerk@gmail.com")


session.add(user1)
session.commit()


user2 = User(name="Ahmad", email="otbsaudm@gmail.com")


session.add(user2)
session.commit()


# Creating categories and items
category1 = Category(name="Sports")


session.add(category1)
session.commit()


item1_1 = Item(name="Football", description="Football is one of the most \
pouplar sports in the world, it is also known as 'The Beautiful Game'.",
               user=user1, category=category1)


session.add(item1_1)
session.commit()


item2_1 = Item(name="Basketball", description="Basketball is a \
leading sport in the United States Of America,\
its players are some of the highest paid in the world.",
               user=user1, category=category1)


session.add(item2_1)
session.commit()


category2 = Category(name="Food")


session.add(category2)
session.commit()


item1_2 = Item(name="Shephard's Pie", description="Shephards Pie a traditional\
British foods, consisting of minced beef/lamb, \
vegetables and covered with a thick layer of \
mashed potatoes before going into the oven.",
               user=user1, category=category2)


session.add(item1_2)
session.commit()


item2_2 = Item(name="Onion Soup", description="Onion Soup is a traditional\
dish from the French cuisine, it need A LOT of onions to make.\
Mostly common in winter, \
Onion Soup is a stable in France.",
               user=user1, category=category2)


session.add(item2_2)
session.commit()


category3 = Category(name="Destinations")


session.add(category3)
session.commit()


item1_3 = Item(name="Dubai", description="Famous for its warm sunny weather\
, great shopping malls and refreshing water adventures,\
Dubai is one of the hottest destinations for summer.",
               user=user1, category=category3)


session.add(item1_3)
session.commit()


category4 = Category(name="Cars")


session.add(category4)
session.commit()


item1_4 = Item(name="BMW", description="BMW is a giant in the cars industry, \
the german company is a leading company in this \
fiels as well as motorcycle production.",
               user=user1, category=category4)


session.add(item1_4)
session.commit()


category5 = Category(name="Phones")


session.add(category5)
session.commit()


item1_5 = Item(name="iPhone X", description="The iPhone X \
was a huge gamble from Apple,\
losing the home button and \
altering the design was a dangerous move,\
but one that was sorely needed \
after years of similarity and the premium design, \
extra power, all-screen front mix together to create. \
with a great screen and strong design iPhone X\
is certainly on of the best Apple ever created.",
               user=user1, category=category5)


session.add(item1_5)
session.commit()


item2_5 = Item(name="Google Pixel", description="Google Pixel is a line of \
consumer electronic devices developed by \
Google that run either Chrome OS or the Android\
operating system. The Pixel brand was introduced in \
February 2013 with the first generation Chromebook Pixel. \
The Pixel line includes laptops, tablets, and smartphones,\
as well as several accessories.",
               user=user1, category=category5)


session.add(item2_5)
session.commit()


category6 = Category(name="Social Media")


session.add(category6)
session.commit()


item1_6 = Item(name="Youtube", description="YouTube is the \
leading video playing,\
sharing and streaming website in the world.",
               user=user1, category=category6)


session.add(item1_6)
session.commit()


item2_6 = Item(name="Twitter", description="Twitter is on of the most \
popular social media \
applications with feeds, hashtags, \
and followers and followings. \
It even got better after adding the dark mode.",
               user=user1, category=category6)


session.add(item2_6)
session.commit()


item3_6 = Item(name="Snapchat", description="Snapchat has \
become notable for representing a new, \
mobile-first direction for social media, \
and places significant emphasis on users \
interacting with virtual stickers and augmented reality objects.\
As of February 2018, Snapchat has 187 \
million daily active users.",
               user=user1, category=category6)


session.add(item3_6)
session.commit()


item4_6 = Item(name="Instagram", description="Instagram also known as IG is a\
photo and video-sharing social\
 networking service owned by Facebook, \
Inc. It was created by Kevin Systrom \
and Mike Krieger, and launched in \
October 2010 exclusively on iOS. \
A version for Android devices was released \
a year and 6 months later, \
in April 2012, followed by a feature-limited \
website interface in November \
2012, and apps for Windows 10 Mobile and Windows \
10 in April 2016 and October 2016 respectively.",
               user=user1, category=category6)


session.add(item4_6)
session.commit()


print "Added categories and items!"
