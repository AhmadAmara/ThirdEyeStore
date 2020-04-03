from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
##--
from user_admin.functions import handle_uploaded_file  
from user_admin.form import StudentForm  
from user_admin.form import LoginForm ,SignUpForm 
from django.shortcuts import redirect
from .models import User
from .models import UserIn

from .models import Category
# for redirect
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def home(request):

    return render(request, "home.html", {})

def about(request):
    
    d = {"l":
         [55, 66, [77, 88], 8	, datetime.now()]
         }
    return render(request, "about.html", d)

def index(request):  
    if request.method == 'POST':  
        student = StudentForm(request.POST, request.FILES)  
        if student.is_valid():  
            handle_uploaded_file(request.FILES['file'])  
            return HttpResponse("File uploaded successfuly")  
    else:  
        student = StudentForm()  
        return render(request,"index.html",{'form':student})


def login(request):  
    if request.method == 'POST':
        #Get the posted form
        MyLoginForm = LoginForm(request.POST)
        if MyLoginForm.is_valid():
            email = MyLoginForm.cleaned_data['email']
            password = MyLoginForm.cleaned_data['password']

            email_value = User.objects.filter(email=email).values()

            if(not email_value):
                return render(request, "signup.html")
            
            elif(email_value[0]['password'] != password):
                return render(request, 'loggedin.html', {"email" : "bad user name","password":"bad password"})        

            else:
                return render(request,'home.html',email_value[0])
            
        else:
            return render(request, 'loggedin.html', {"email" : "bad user name","password":"bad password"})        
    else:
     return render(request, 'loggedin.html', {"email" : "email","password":"nopassword"})

def signup(request):
    if request.method == 'POST':
        #Get the posted form
        MySignupForm = SignUpForm(request.POST)
        if MySignupForm.is_valid():
            email = MySignupForm.cleaned_data['email']
            password = MySignupForm.cleaned_data['password']
            rep_password = MySignupForm.cleaned_data['rep_password']

            email_value = User.objects.filter(email=email).values()
            
            if(email_value):
                return render(request, "signup.html", {'email': email ,'bademail':'bademail', 'message': 'this email already signedup'})

            new_user = User()
            new_user.email = email
            new_user.password = password
            new_user.save()
            return render(request, "welcome.html")
        else:
            return render(request, "home.html")        
    else:
        return render(request, "signup.html",{})

        
def welcome(request):
    return render(request, "welcome.html",{"email" : "badwelcome"} )



def categories(request):
    all_items = Category.objects.all
    return render(request, "categories.html", {'all_items': all_items})


def category(request,category_id):
    
    return render(request, "category.html", {'all_items': category_id})

def signout(request):
    return render(request, "home.html")

def forgotten_password(request):
    return render(request, 'forgotten_password.html')

