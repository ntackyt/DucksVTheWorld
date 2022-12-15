"""
Definition of views.

Resources used:
https://stackoverflow.com/questions/34968413/error-index-not-defined-add-indexon

"""
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponse
from app import forms
from .forms import BootstrapAuthenticationForm, BootstrapRegisterForm
from django.core.files.storage import default_storage

# To interface with Google Firebase
import pyrebase
# For RegEx for email validation
import re 
# For parsing database queries
import json

# Testing to see if databse items match local values in the session
def check_user_data(request, user_id):
    user_db_data = db.child("Data").child("Users").order_by_child("user_id").equal_to(user_id).get()
    # Put results in list format
    user_data = list(user_db_data.val().items())[0]

    for key, value in user_data[1]['user_data'].items():
        value_name = key
        local_value = request.session['current_user_data'][value_name]
        if (local_value != value):
            return False
    return True


# Variables to authenticate firebase
firebaseConfig = {
  "apiKey": "AIzaSyAEAeGmrnWjANDIdSItht4fsJI2AtzE7oQ",
  "authDomain": "ducksvstheworld-d7723.firebaseapp.com",
  "databaseURL": "https://ducksvstheworld-d7723-default-rtdb.firebaseio.com",
  "projectId": "ducksvstheworld-d7723",
  "storageBucket": "ducksvstheworld-d7723.appspot.com",
  "messagingSenderId": "753675718519",
  "appId": "1:753675718519:web:eef8ee7eefb758a7b9db72",
  "measurementId": "G-CX8L0Z3XT3"
}


# Firebase authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

# validate that a given string is an email
def validate_email(email):
    regex = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'

    if (re.fullmatch(regex, email)):
        return True
    else:
        return False

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    
    return render(
        request,
        'app/home.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'current_user': auth.current_user
        }
    )

def login(request):
    # Rendering login page
    assert isinstance(request, HttpRequest)

    # Form to display on login.html
    form = BootstrapAuthenticationForm()

    return render(
        request,
        'app/login.html',
        {
            'year': datetime.now().year,
            'form':form
        }
    )

def postlogin(request):
    email=request.POST.get('email')
    password=request.POST.get('password')

    form = BootstrapAuthenticationForm()
    try:
        # if there is no error then signin the user with given email and password
        # user=authe.sign_in_with_email_and_password(email,pasw)
        user = auth.sign_in_with_email_and_password(email, password)

    except:
        message="That email and password is invalid. Please submit a correct username and password."
        return render(request,"app/login.html", {'message':message, 'current_user': auth.current_user, "form":form})

    # set current session with user token
    session_id=user['idToken']
    request.session['uid']=str(session_id)
   
    # get current user's data from database
    user_db_data = db.child("Data").child("Users").order_by_child("user_id").equal_to(user['localId']).get()

    # if user data is not in database, then throw error message
    if not user_db_data.val():
        message="No user data in database. Contact administrator at ducksvstheworld@gmail.com"
        return render(request,"app/login.html", {'message':message, 'current_user': auth.current_user, "form":form})
    user_data = list(user_db_data.val().items())[0]
    
    # set user data to current session
    request.session['user_push_id'] = user_data[0]
    request.session['localId'] = user['localId']
    request.session['email'] = email
    request.session['current_user'] = auth.current_user
    request.session['current_user_data'] = user_data[1]['user_data']


    return render(request,"app/home.html", {"email":email, 'current_user': auth.current_user})
 
def signup(request):
    assert isinstance(request, HttpRequest)

    form = BootstrapRegisterForm()

    return render(request, "app/signup.html", {'form':form})

def postsignup(request):
     email = request.POST.get('email')
     password1 = request.POST.get('password1')
     password2 = request.POST.get('password2')
     first_name = request.POST.get('first_name')
     last_name = request.POST.get('last_name')
     form = BootstrapRegisterForm()
     message = ""

     # Handle these cases on our side to reduce needless HTTP requests
     # If email entered isn't actually an email, then reload page and return error msg
     if (validate_email(email) == False):
         message = "Please enter a valid email."
         return render(request, "app/signup.html", {'message':message, 'form':form})

     # If passwords don't match, then reload page and return error msg
     if (password1 != password2):
         message = "Both passwords must match."
         return render(request, "app/signup.html", {'message':message, 'form':form})

     # If password isn't longer than 5 characters, then reload page and return error msg
     if (len(password1) < 6):
         message = "Password must be at least 6 characters."
         return render(request, "app/signup.html", {'message':message, 'form':form})

     # If all tests pass, try to create user
     try:
        # Create a user with the given email and password
        user = auth.create_user_with_email_and_password(email, password1)
     except Exception as e:
        # Let Firebase handle this error as it's hard to check for on our side
        if ("EMAIL_EXISTS" in e.args[1]):
            message = "An account has already been created with that email."
        else:
            message = "An error has occurred. Please try again later."

        # If error, then return to signup page
        return render(request, "app/signup.html", {'message':message, 'form':form})
    
     
     # push user data to database
      # Pass the user's idToken to the push method
      # data to save
     data = {
        "user_id": user['localId'],
        "user_data": {
            "first_name": first_name,
            "last_name": last_name,
            "num_ducks": 0,
            "num_points": 0,
            "prof_desc": "",
            "prof_pic": storage.child("prof_pics/default_prof_pic.jpg").get_url(None)
            }
     }
     
     results = db.child("Data").child("Users").push(data)
     
     # If user was created successfully, redirect to login page
     return redirect("login")

def logout(request):
    try:
        del request.session['uid']
        del request.session['user_push_id']
        del request.session['localId']
        del request.session['email']
        del request.session['current_user']
        del request.session['current_user_data']
        auth.current_user = None
    except:
        pass

    return redirect("login")

def contact(request):
    """Renders the contact page."""

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def show_user_profile(request, user_id):
    assert isinstance(request, HttpRequest)

    # Make sure user is logged in before testing to redirect to their profile page
    if (request.session.get('localId') != None):
        # If the user is trying to get to their own profile, then show them their profile page where they can edit attributes
        if (user_id == request.session['localId']):
            return redirect("profile")

    error_msg = ""
    user_data = []
    # Get data from user to display on profile page
    try:
        user_db_data = db.child("Data").child("Users").order_by_child("user_id").equal_to(user_id).get()
        # Put results in list format
        user_data_list = list(user_db_data.val().items())[0]
        user_data = user_data_list[1]['user_data']
    except:
        error_msg = "That is not a valid user."

    try:
         # Get all Posts from user
        user_db_pins = db.child("Data").child("Posts").order_by_child("pin_user_id").equal_to(user_id).get()
    
        user_pin_data = [] # python list
        for pin in user_db_pins.each():
            user_pin_data.append(pin.val())
    except:
        error_msg = "Could not load posts of user."

    return render(request, "app/show_user_profile.html", {'user_data':user_data, 'pins':user_pin_data, 'error_msg': error_msg})




def profile(request):
    assert isinstance(request, HttpRequest)

    # Make sure user is logged in
    if (request.session.get("localId") == None):
        return render(request, "app/profile.html", {'success':False, 'error_msg':" You are not signed in", "pins": []})


    # Get all Posts from user
    user_db_pins = db.child("Data").child("Posts").order_by_child("pin_user_id").equal_to(request.session['localId']).get()
    
    user_pin_data = [] # python list
    for pin in user_db_pins.each():
        user_pin_data.append(pin.val())

    # To get the push id for the current user, as that is what the user data is filed under in JSON format
    current_user_push_id = request.session['user_push_id']

    # Save file to local machine so it can be uploaded to Firebase
    error_msg = ""
    success = True

    # If we got an POST request from an ajax command
    # i.e., if a user edited an attribute on the profile page
    attribute_type = request.POST.get("attribute_type")
    if request.method == 'POST' and attribute_type != None:
        

       
        # If we are getting an ajax request, then we are just getting text values
        new_value = request.POST.get("new_value")
        old_value = request.POST.get("old_value")

        try:
            db.child("Data").child("Users").child(current_user_push_id).child("user_data").update({attribute_type: new_value})  
        except Exception as e:
            error_msg = e.args[1]
            success = False

        # Update session first name value if successful
        if (success == True):
            request.session['current_user_data'][attribute_type] = new_value
            # Tells Django to that we made a change to a session variable and to update it
            request.session.modified = True
    
        # Return 200 OK with json data about success of update operation
        return HttpResponse(json.dumps({'success': success, 'attribute_type':attribute_type, 'error_msg': error_msg, 'old_value': old_value}), content_type="application/json");
    elif request.method == 'POST':
        # If we are getting a profile pic
        # https://dev.to/mdrhmn/django-firebase-cloud-storage-331p
        
        # Get new profile picture
        file = request.FILES.get("file")
        
        # Make sure file is a picture 
        file_extension = file.name.split('.')[-1]  

        if (file_extension != "jpg" and file_extension != "png" and file_extension != "jpeg"):
            error_msg = "You must upload an image file. Only png, jpg, and jpeg are allowed."
            return render(request, "app/profile.html", {'success':False, 'error_msg':error_msg})

        # Add user id to end of file to prevent same file names overwriting other users pictures
        new_file_name = file.name + request.session['localId']
        
        try:
            default_storage.save(new_file_name, file)
            # Upload profile pic to Firebase
            storage.child("prof_pics/" + new_file_name).put(new_file_name, request.session['localId'])
            # Delete file from local machine
            default_storage.delete(new_file_name)

            
        except Exception as e:
            error_msg = e.args[1]
            success = False

        # Get the url of the new picture
        new_url = storage.child("prof_pics/" + new_file_name).get_url(request.session['localId'])
        # Update profile pic url in database
        db.child("Data").child("Users").child(current_user_push_id).child("user_data").update({"prof_pic": new_url})  

        # Update session first name value if successful
        if (success == True):
            request.session['current_user_data']["prof_pic"] = new_url
            # Tells Django to that we made a change to a session variable and to update it
            request.session.modified = True

        # Return profile with new data
        return render(request, "app/profile.html", {'success':True, 'error_msg':"", "pins": user_pin_data})

    return render(request, "app/profile.html", {'success':True, 'error_msg':"", "pins": user_pin_data})



def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'year':datetime.now().year,
        }
    )

def whatwedo(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/whatwedo.html',
        {
            'title':'What We Do',
            'year':datetime.now().year,
        }
    )

def game(request):
    """Renders the games page."""
    assert isinstance(request, HttpRequest)

    error_msg = ""
    # Make sure that the user is logged in before awarding points

    try:
        request.session['localId']
    except Exception as e:
        error_msg = "You are not signed in, so points cannot be awarded."
        
    if request.method == 'POST' and error_msg == "":

        # To get the push id for the current user, as that is what the user data is filed under in JSON format
        current_user_push_id = request.session['user_push_id']
        current_user_local_id = request.session['localId']

        # get the points earned
        points_earned = request.POST.get("points_earned")

        # If we are getting an ajax request, then we are just getting text values
        old_points = db.child("Data").child("Users").order_by_child("user_id").equal_to(current_user_local_id).get()
        old_points_list = list(old_points.val().items())[0]
        points_earned = int(points_earned) + int(old_points_list[1]['user_data']['num_points'])

        
        success = True
        try:
            db.child("Data").child("Users").child(current_user_push_id).child("user_data").update({"num_points": points_earned})  
        except Exception as e:
            error_msg = "Could not update user points."
            success = False

        # Update session first name value if successful
        if (success == True):
            request.session['current_user_data']['num_points'] = points_earned
            # Tells Django to that we made a change to a session variable and to update it
            request.session.modified = True

    return render(
        request,
        'app/game.html',
        {
            'title':'Games',
            'error_msg': error_msg
        }
    )

def map(request):
    """Renders the map page."""
    assert isinstance(request, HttpRequest)

    # Get all posts from database
    user_db_pins = db.child("Data").child("Posts").get() #returns pyrebase object
   
    
    pin_data = [] # python list 
    pin_data_w_user = []
    for pin_id in user_db_pins.each():
        # Get user data for the user associated with this pin
        pin_user_id = pin_id.val()["pin_user_id"]
        user_db_data = db.child("Data").child("Users").order_by_child("user_id").equal_to(pin_user_id).get()
        user_data = list(user_db_data.val().items())[0]

        # Add this user data to the dictionary to send to the webpage
        pin_data_w_user = pin_id.val()
        pin_data_w_user['user_first_name'] = user_data[1]['user_data']['first_name']
        pin_data_w_user['user_last_name'] = user_data[1]['user_data']['last_name']
        pin_data_w_user['user_prof_pic'] = user_data[1]['user_data']['prof_pic']

        # Append dictionary to list of dictionaries holding lists of pins
        pin_data.append(pin_data_w_user)
 
    pins_json = json.dumps(pin_data) # convert to json format
    return render(request, 'app/map.html', {'curr_pins' : pins_json})
    

def add_pin(request):
     pin_name = request.POST.get('pin_name')
     pin_type_bool = request.POST.get('pin_type_str')
     pin_addr = request.POST.get('pin_addr')
     pin_date = request.POST.get('pin_date')
     pin_desc = request.POST.get('pin_desc')
     pin_lat = request.POST.get('pin_lat')
     pin_lng = request.POST.get('pin_lng')
     pin_points =  request.POST.get('pin_points')

    # get the old point and update them
     try:
        current_user_push_id = request.session['user_push_id']
        current_user_local_id = request.session['localId']
     except Exception as e:
        error_msg = e.args[1]
        return redirect("map")

     old_points = db.child("Data").child("Users").order_by_child("user_id").equal_to(current_user_local_id).get()
     old_points_list = list(old_points.val().items())[0]

    # Convert to int
     if pin_points == "":
         pin_points = 400
     elif pin_points == "400":
        pin_points = 400
     else: 
        pin_points = 600
     success = True
     # Get the updated points
     user_points = pin_points + old_points_list[1]['user_data']['num_points']
   
     try:
        db.child("Data").child("Users").child(current_user_push_id).child("user_data").update({"num_points": user_points})  
     except Exception as e:
        error_msg = e.args[1]
        success = False

     # If we successfully added the user points, then change local variable as well
     if success == True:
         request.session['current_user_data']['num_points'] = user_points
         request.session.modified = True
    
     data = {
        "pin_name": pin_name,
        "pin_user_id": request.session['localId'],
        "pin_data": {
            "pin_type_bool": pin_type_bool,
            "pin_addr": pin_addr,
            "pin_date": pin_date,
            "pin_desc": pin_desc,
            "pin_lat": pin_lat,
            "pin_lng": pin_lng,
            "pin_points": pin_points,
            }
     }

    
     # Add the pin data to the database
     results = db.child("Data").child("Posts").push(data)

     return redirect("map")


