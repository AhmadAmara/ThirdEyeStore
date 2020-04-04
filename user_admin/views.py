from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
##--
from user_admin.functions import handle_uploaded_file  
from user_admin.form import StudentForm  
from user_admin.form import LoginForm ,SignUpForm,Order
from django.shortcuts import redirect
from .models import User,Product,Order_Line,Cart

from .models import Category
# for redirect
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def home(request):
    return render(request, 'home.html', {'email':''})

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
     return render(request, 'loggedin.html')

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
            return render(request, "loggedin.html")
        else:
            return render(request, "signup.html",{'message': 'somthing wrong, please fill the form again'})        
    else:
        return render(request, "signup.html",{})

        
def welcome(request):
    return render(request, "welcome.html",{"email" : "badwelcome"} )



def categories(request):
    all_items = Category.objects.all
    return render(request, "categories.html", {'all_items': all_items})


def category(request,category_id):
    if request.method == 'POST':
      print("koko")
      print(request.POST)
      OrderForm = Order(request.POST)
      print(OrderForm)
     # if OrderForm.is_valid():
     #   productid = OrderForm.cleaned_data['ProdectID']
     #   print(productid)
      #return redirect('addcard')
    Products = Product.objects.filter(category=category_id).values()
    return render(request, "category.html",{'category_id':category_id,'all_items': Products})

def signout(request):
    return render(request, "home.html")
def addorder(request,Product_id):
    new_user = User()
    new_user.email = "koko@emil.com"
    new_user.password = "password"
    new_user.save()
    product = Product.objects.get(pk=Product_id)
    cat=product.category.catName
    
    new_order=Order_Line()
    c=Cart()
    c.User_em=new_user
    c.save()
    new_order.CardId=c
    new_order.ProductID=product
    new_order.price=product.price
    new_order.save()
    return redirect('../category/'+cat)
    #return render(request,cat+"/category.html")

def forgotten_password(request):
    return render(request, 'forgotten_password.html')
def cart(request):
    all_items = Order_Line.objects.all()
    return render(request, 'cart.html', {'all_items': all_items})

