# SW_DuckiesVJohnWick

# Introduction:

# Team Members:
Rachel Chambers, Naomi Tack, Dinora Blanco, Scott Witschey, and Shreyansh Kumar

# Website:
To view the above code, please visit our website!
http://ducksvstheworld.pythonanywhere.com/

Note: For the current implementtaion of Ducky Goes to Space the connection must be *http* as https blcks the connection to an http site.

# File Structure:

Django projects made with Visual Studio follow a specific file structure. The main code is in app/views.py, a Python file which holds logic to send posts and user data to the database, sign in and register users, and render HTML pages populated by data from our database. We also use Javascript. One important JS file is at app/static/app/modules/map.js, which holds the Javascript for the map page. The JS file at app/static/app/scripts/profile_script.js is also important, as it holds the code for the profile page. All the HTML files rendered by Django using Jinja markup are in app/templates/app.

You also want to look at app/tests.py which contain unit tests to make sure pages load correctly. If you download our project and install Django and Python and then go to the project folder where manage.py is stored, you can run ```python manage.py test``` and run the tests in tests.py. 

Here are the important files and their folder structure:

```
└─── manage.py 
    -- when run, starts the Django server 
└─── DuckiesVsJohnWick
  └─── settings.py
    -- settings for Django
  └─── urls.py
    -- registers urls with view functions (such as registering <website url>/profile/ with the views.py function "profile")
  └─── wsgi.py
    -- settings for WSGI (how server communicates with Python framework)
└─── app
  └─── forms.py
    -- holds Django forms (only sign up and login, as those are the forms that use the Django forms framework)
  └─── views.py
    -- Holds the code rendering each page of the website as well as authentication and profile backend, handles all database calls
  └─── tests.py
    -- Holds unit tests for making sure pages load correctly
  └─── static
    └─── app
        └─── content
          -- holds css files
        └─── fonts
          -- holds fonts
        └─── modules
          -- holds javascript for map page
        └─── scripts
          -- holds all javascript files (minus map page)
  └─── templates
    └─── app
      -- hold all .html files (rendered with Jinja)
```

# Local Installation:

Go to our GitHub page and export our project files (clone or download the zip) into a workspace folder: 

https://github.com/ntackyt/DucksVTheWorld.git

Through terminal (or VSCode’s terminal), move into the workspace folder. From there, you can do the following steps to install the virtual environment and the rest of the dependents. From there you should be able to run the site: 

## <b>Django and Python Installation</b> 

**Windows:**

1. If python is not already installed, install python 3.10, which should come with pip. Follow the installation instructions and check if it’s correctly installed by typing: 
```
python –version 
```
2. Install and set up a virtualenv:    
```
python –m pip install virtualenv 
python –m venv venv 
```

3. Enter the command prompt terminal (specifically cmd instead of powershell if you're on visual studio code, click on the right side icon of vscode's terminal window to change it). Then type in:
```
.\venv\Scripts\activate
```

4. Install the extensions. Please note that it MUST be pyrebase 4. (Note: this only has to be done the first time you enter the virtual enviroment.)
```
python -m pip install django 
python -m pip install pyrebase4 
```

5. Once you’ve installed these dependents, you can run a devolpment server. The simplest way it thought the command terminal: 
```
python manage.py runserver
```
(Make sure you’re within the folder that has manage.py - this should be the main folder of the repository.)
The file system should look like this:
```
SW_DuckiesVTheWorld
  - app/
  - DuckiesVJohnWick/
  -.venv/
  - ...
  -manage.py
```
Alternatively you can put the <i>.venv</i> folder outside of the <i>SW_DuckiesVTheWorld</i> and cd into it to then the <i>python manage.py runserver</i>
  
6. Copy the server port and open it in either Google Chrome or Microsoft Edge.

7. To deactivate the virtual environment, either close the terminal or type:
```
deactivate
```
8. To rerun the window follow steps 3, 5 and 6:
```
.\venv\Scripts\activate
python manage.py runserver
```
