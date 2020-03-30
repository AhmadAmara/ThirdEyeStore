from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
##--
from user_admin.functions import handle_uploaded_file  
from user_admin.form import StudentForm  
from user_admin.form import LoginForm  
from django.shortcuts import redirect
from .models import List
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
            username = MyLoginForm.cleaned_data['username']
            password = MyLoginForm.cleaned_data['password']
            #your code using database
            if username=='Ahmad':
              #return redirect('welcome') # just to request first time the page
              return render(request,'welcome.html',{"username" : username})
            else:
              return render(request, 'loggedin.html', {"username" : username,"password":password})
        else:
            return render(request, 'loggedin.html', {"username" : "bad user name","password":"bad password"})        
    else:
     return render(request, 'loggedin.html', {"username" : "nousername","password":"nopassword"})


def welcome(request):
    return render(request, "welcome.html",{"username" : "badwelcome"} )


def categories(request):
    return render(request, "categories.html")


def signout(request):
    return render(request, "home.html")

def forgotten_password(request):
    return render(request, 'forgotten_password.html')

