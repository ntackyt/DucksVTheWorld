# SW_DuckiesVJohnWick

# Introduction:

# Team Members:
Rachel Chambers, Naomi Tack, Dinora Blanco, Scott Witschey, and Shreyansh Kumar

# References:


# Installation:

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
