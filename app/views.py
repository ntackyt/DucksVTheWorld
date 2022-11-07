"""
Definition of views.

Resources used:
https://stackoverflow.com/questions/34968413/error-index-not-defined-add-indexon

"""
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from app import forms
from .forms import BootstrapAuthenticationForm, BootstrapRegisterForm

# To interface with Google Firebase
import pyrebase
# For RegEx for email validation
import re 
# For parsing database queries
import json

# Variables to authenticate firebase


firebaseConfig = {
  "apiKey": "insert API here",
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
    
    data1 = {"email":"meeeeeeee@gmail.com","password":"me"}
    db.child("Data").push(data1)
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
    for user in user_db_data.each():
        print("KEY:", user.key()) # Morty
        print("VALUE:", user.val()) # {name": "Mortimer 'Morty' Smith"}
        print(type(user.val()))
        print(dict(user.val()))

    # if user data is not in database, then throw error message
    if not user_db_data.val():
        message="No user data in database. Contact administrator at ducksvstheworld@gmail.com"
        return render(request,"app/login.html", {'message':message, 'current_user': auth.current_user, "form":form})
    first_item = list(user_db_data.val().items())[0]
    print(first_item[0])
    print(first_item[1]['user_data'])
    # set user data to current session
    request.session['email'] = email
    request.session['current_user'] = auth.current_user
    request.session['current_user_data'] = first_item[1]['user_data']


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
            "num_ducks": 0,
            "num_points": 0
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
        authe.current_user = None
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

