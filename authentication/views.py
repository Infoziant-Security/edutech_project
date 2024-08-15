from pyexpat.errors import messages
from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
         
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/signin/')
         
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
         
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return render(request, "/signin/")
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('/jobseekerhome/')
    return render(request, "login.html")

def register(request):
    if request.method=='POST':
        
        email=request.POST['email']
        password=request.POST['password']
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=email)
         
        if user.exists():
            # Display an information message if the username is taken
            
            return redirect('/register/')
         
        # Create a new User object with the provided information
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        # save the user object
        user.save()
        return render(request, "/login/")
    return render(request, "register.html")

def jobseekerhome(request):
    return render(request,"jobseekerhome.html")
