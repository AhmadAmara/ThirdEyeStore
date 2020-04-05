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
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, "about.html")

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
                d=dict(email_value[0])
                request.session['logged_in'] = True
                request.session['email']=d['email']
                request.session['typ']=d['typ']
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

            email_value = User.objects.filter(email=email).values()
            
            if(email_value):
                return render(request, "signup.html", {'email': email ,'bademail':'bademail', 'message': 'this email already signedup'})

            new_user = User()
            new_user.email = email
            new_user.password = password
            new_user.save()
            c=Cart()
            c.User_em=new_user
            c.save()

            return render(request, "loggedin.html")
        else:
            return render(request, "signup.html",{'message': 'somthing wrong, please fill the form again'})        
    else:
        return render(request, "signup.html",{})

        
def welcome(request):
    return render(request, "welcome.html",{"email" : "badwelcome"} )



def categories(request):
    all_items = Category.objects.filter
    return render(request, "categories.html", {'all_items': all_items})


def category(request,category_id):
    if request.method == 'POST':
    #   print("koko")
    #   print(request.POST)
      OrderForm = Order(request.POST)
    #   print(OrderForm)
     # if OrderForm.is_valid():
     #   productid = OrderForm.cleaned_data['ProdectID']
     #   print(productid)
      #return redirect('addcard')
    Products = Product.objects.filter(category=category_id).values()
    return render(request, "category.html",{'category_id':category_id,'all_items': Products})

def signout(request):
    try:
        del request.session['logged_in']
        del request.session['email']
        del request.session['typ']
    except KeyError:
        pass
    return render(request, "home.html")

def addorder(request,Product_id):
    if request.session.get('logged_in'):
        product = Product.objects.get(pk=Product_id)
        cat=product.category.catName
        user = User.objects.get(pk=request.session['email'])
        c=Cart.objects.filter(User_em=request.session['email']).get(isCheckout=False)
        ol=Order_Line.objects.filter(CartId=c).filter(ProductID=product)
        if (ol):
            ol=Order_Line.objects.filter(CartId=c).get(ProductID=product)
            ol.Quantity=ol.Quantity+1
            ol.save()
        else :
            new_order=Order_Line()
            new_order.CartId=c
            new_order.ProductID=product
            new_order.price=product.price
            new_order.save()
    
        return redirect('../category/'+cat)
    else:
        return render(request, 'loggedin.html')


def delol(request,ol_id):
    if request.session.get('logged_in'):
        ol = Order_Line.objects.get(pk=ol_id)
        print(ol)
        ol.delete()
        # messages.success(request, ('Item Has Been Deleted!'))
        return redirect('../cart/')
    else:
        return render(request, 'loggedin.html')

def forgotten_password(request):
    return render(request, 'forgotten_password.html')

def cart(request):

    if request.session.get('logged_in'):
        cartid = Cart.objects.filter(User_em=request.session['email']).get(isCheckout=False)
        ord_lin = Order_Line.objects.filter(CartId=cartid)
        total_price=0
        for ol in ord_lin :
            total_price += ol.Quantity * ol.price
        return render(request, 'cart.html', {'all_items': ord_lin, 'total_price': total_price})
    else:
        return render(request, 'home.html')


