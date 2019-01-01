# Introduction 

In this project I was asked to create an Item Catalog Application which has a catalog that contains categories and each category contains items. Users should be able to perform the CRUD functionality on the items in the Item Catalog. I was asked to create at least one JSON API Endpoint in the application.
Users should be able to add items when they are logged in, items could be edited and deleted **only** by the user who added them. I was asked to use google's sign in as a third party authentication.

# Installation 

Here are all the things you will need to install before you run this application:

* You will need to install VirtualBox from [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).
* You will need to install Vagrant from [here](https://www.vagrantup.com/downloads.html).
* To download the Virtual Machine you can download and unzip [this file](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip), which will give you a directory called FSND-Virtual-Machine. It may be located inside your Downloads folder, we were asked to work within the 'category' folder.
* Alternatively, you can use Github to fork and clone [this repository](https://github.com/udacity/fullstack-nanodegree-vm).


# Execution 

After downloading and installing the required files and tools above, follow these steps to run the application:

1. Change to the directory having the VM files (The zip folder) in your terminal using the `cd` command followed by the name of the file you to change into. You will find another directory called vagrant. `cd` into the vagrant directory. 
2. Then, change into the 'catalog' directory using the same command `cd`.
3. Start you Virtual Machine using `vagrant up` and when it is finished running, run the `vagrant ssh` command to login to your VM.
4. Now we just have to run the python program, to do that just make sure you are in the directory 'catalog' which contains the python file, just run `python "ItemCatalogProject.py"`. 
5. Now the program should be running.
6. Open a browser window and and type `http://localhost:8000` , 8000 is the port number the server is listening on.


# Code Design 

When writing the python code I followed a python formatting style that was required by Udacity using a command line tool, the tool is pycodestyle. 
To install this tool I used the `pip3 install pycodestyle` command. 
Functions included in the `ItemCatalogProject.py` code are (excluding the google authentication functions): 
- `showCatalog()` which shows all the categoris in the item catalog and the latest 10 added items.
- `showCategory()` which shows the selected category's items.
- `showItem()` which shows the selected item's information.
- `addItem()` which is used to add a new item to the item catalog.
- `editItem()` which is used to modify the selected item's information.
- `deleteItem()` which is used to delete the selected item from the item catalog.
I have also created some JSON Endpoints which can be found in the following functions:
- `catalogJSON()` which shows the categories in the item catalog in a JSON serialized format.
- `categoryJSON()` which show the category items in a JSON serialized format.



# Notes 

In the `database_setup.py` file, the database consists of 3 tables:
1. The `User` table which has the columns (id,name,email) and is used to store the application's users.
2. The `Category` table which has the columns (id,name) and (user_id) as foreign key to the id column in the `User` table.
3. The `Item` table which has the columns (id,name,description) and (user_id) as foreign key to the id column in the `User` table also (category_id) as foreign key to the id column in the `Category` table.


# References 

* I have used [this](https://stackoverflow.com/questions/15435811/what-is-pep8s-e128-continuation-line-under-indented-for-visual-indent) feed from **StackOverFlow** to help me with meeting the wanted styling requirements in PEP8.
* I have used the class activity _startup_ example to help me with setting up the google authentication correctly.
* I have used some elements from [Bootstrap](https://getbootstrap.com) to help me with the front-end design.
* I have used [uiGradients](https://uigradients.com/#BlueRaspberry) to help me with the front-end design.
