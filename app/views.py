"""
Definition of views.

Resources used:
https://stackoverflow.com/questions/34968413/error-index-not-defined-add-indexon

"""
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from app import forms
from .forms import BootstrapAuthenticationForm, BootstrapRegisterForm
from django.core.files.storage import default_storage

# To interface with Google Firebase
import pyrebase
# For RegEx for email validation
import re 
# For parsing database queries
import json

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
    
    #accessing our firebase data and storing it in a variable
    '''userid = database.child('Data').child('id').get().val()
    #username = database.child('Data').child('username').get().val()
    
   # print("********************************************************")
    print(userid)
    print(username)

    context = {
        'id':userid,
        'username':username,
        }

    print("user is anonomys")
    print(request.user.is_anonymous)
    '''
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
    print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
    print(email, password)
    try:
        # if there is no error then signin the user with given email and password
        # user=authe.sign_in_with_email_and_password(email,pasw)
        user = auth.sign_in_with_email_and_password(email, password)
        print("email", email, "password", password)
        print(user)
        print(auth.current_user)

    except:
        message="That email and password is invalid. Please submit a correct username and password."
        return render(request,"app/login.html", {'message':message, 'current_user': auth.current_user, "form":form})

    # set current session with user token
    session_id=user['idToken']
    request.session['uid']=str(session_id)
   

    # get current user's data from database
    user_db_data = db.child("Data").child("Users").order_by_child("user_id").equal_to(user['localId']).get()
    for user1 in user_db_data.each():
        print("KEY:", user1.key()) # Morty
        print("VALUE:", user1.val()) # {name": "Mortimer 'Morty' Smith"}
        print(type(user1.val()))
        print(dict(user1.val()))

    # if user data is not in database, then throw error message
    if not user_db_data.val():
        message="No user data in database. Contact administrator at ducksvstheworld@gmail.com"
        return render(request,"app/login.html", {'message':message, 'current_user': auth.current_user, "form":form})
    user_data = list(user_db_data.val().items())[0]
    print("first item: ", user_data[0])
    print("first item 1[userdata]", user_data[1]['user_data'])
    print("local id", user['localId'])
    # set user data to current session
    request.session['user_push_id'] = user_data[0]
    request.session['localId'] = user['localId']
    request.session['email'] = email
    request.session['current_user'] = auth.current_user
    request.session['current_user_data'] = user_data[1]['user_data']


    '''
    accountinfo = auth.get_account_info(user['idToken'])
    print("ACCCCOUNT INFOOOOOOOOOOOOOOOOOO")
    print(accountinfo)

    # get user data from database
    user_data = db.child("Data").child("Users").child(user["localId"]).get()
    print("USER DATAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(user_data.val()["num_ducks"])
    user_data_dict = user_data.val()\
'''

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
            "prof_desc": ""
            }
     }
     #print(user['idToken'])
     #print(user['localId'])
     results = db.child("Data").child("Users").push(data)
     '''
     results2 = db.child("Data").child("Users").get()
     for user in results2.each():
        print("KEY:", user.key()) # Morty
        print("VALUE:", user.val()) # {name": "Mortimer 'Morty' Smith"}
     # print(results)

     get_current_user = db.child("Data").child("Users").order_by_child("user_id").equal_to("wxfnMRylVtMjI3rsBvI3i2unO7I2").get()
     print(get_current_user.val())
     '''
     # If user was created successfully, redirect to login page
     return redirect("login")

def logout(request):
    try:
        print("LOGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
        del request.session['uid']
        del request.session['']
        del request.session['user_push_id']
        del request.session['localId']
        del request.session['email']
        del request.session['current_user']
        del request.session['current_user_data']
        auth.current_user = None
    except:
        pass
    #return render(request,"app/login.html")
    return redirect("login")

def contact(request):
    """Renders the contact page."""
    print("CONTACCCCCCCCCCCCCCCCCCCTTTTTTTTTTTTTTT")
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

def profile(request):
    results2 = db.child("Data").child("Users").get()
    for user in results2.each():
        print("KEY:", user.key()) # Morty
        print("VALUE:", user.val()) # {name": "Mortimer 'Morty' Smith"}
     # print(results)


    assert isinstance(request, HttpRequest)
    
    pic_url = storage.child("prof_pics/realistic_duck.jpg").get_url(None)

    # If we got an POST request from an ajax command
    # i.e., if a user edited an attribute on the profile page
    if request.method == 'POST' and request.is_ajax():
        attribute_type = request.POST.get("attribute_type")

       
        # If we are getting an ajax request, then we are just getting text values
        new_value = request.POST.get("new_value")
        old_value = request.POST.get("old_value")

        # To get the push id for the current user, as that is what the user data is filed under in JSON format
        current_user_push_id = request.session['user_push_id']
    
        error_msg = ""
        success = True
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
        print("prof_pic")
        # Get new profile picture
        file = request.FILES.get("file")
        
        # Make sure file is a picture 


        # Save file to local machine so it can be uploaded to Firebase
        file_save = default_storage.save(file.name, file)
        # Upload profile pic to Firebase
        storage.child("prof_pics/" + file.name).put(file.name)
        # Delete file from local machine
        delete = default_storage.delete(file.name)
        print()
        #messages.success(request, "File upload in Firebase Storage successful")
        success = True

        return HttpResponse(json.dumps({'success': success}), content_type="application/json");
    return render(request, "app/profile.html", {'success':True, 'error_msg':""})



def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def game(request):
    """Renders the games page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/game.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def game_1(request):
    """Renders the game 1 page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/Game 1/index.html',
        {
            'title':'Game 1',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def game_1_editor(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/Game 1/editor.html',
        {
            'title':'Game 1 editor',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def game_survivor(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/game_survivor.html',
        {
            'title':'Game 1 editor',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def map(request):
    """Renders the map page."""
    assert isinstance(request, HttpRequest)
    user_db_pins = db.child("Data").child("Posts").get() #returns pyrebase object
    pin_data = [] # python list 
    for pin_id in user_db_pins.each():
        pin_data.append(pin_id.val())
    pins_json = json.dumps(pin_data) # convert to json format
    return render(request, 'app/map.html', {'curr_pins' : pins_json})
    

def add_pin(request):
     pin_name = request.POST.get('pin_name')
     pin_type_str = request.POST.get('pin_type_str')
     pin_type_bool = request.POST.get('pin_type_bool')
     pin_addr = request.POST.get('pin_addr')
     pin_date = request.POST.get('pin_date')
     pin_desc = request.POST.get('pin_desc')
     pin_lat = request.POST.get('pin_lat')
     pin_lng = request.POST.get('pin_lng')
     pin_points =  request.POST.get('pin_points')
     trash_pic1 = request.POST.get('trash_pic1')
     trash_pic2 = request.POST.get('trash_pic2')
     
     data = {
        "pin_name": pin_name,
        "pin_data": {
            "pin_type_str": pin_type_str,
            "pin_type_bool": pin_type_bool,
            "pin_addr": pin_addr,
            "pin_date": pin_date,
            "pin_desc": pin_desc,
            "pin_lat": pin_lat,
            "pin_lng": pin_lng,
            "pin_points": pin_points,
            "pin_trash_pic1": trash_pic1,
            "pin_trash_pic2": trash_pic2
            }
     }
     results = db.child("Data").child("Posts").push(data)
     return redirect("map")