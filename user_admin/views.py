from django.shortcuts import render
import datetime
from django.http import HttpResponse
##--
from user_admin.functions import handle_uploaded_file  
from user_admin.form import StudentForm,UserForm ,Editqtyform
from user_admin.form import LoginForm ,SignUpForm,ProductForm,CategoryForm, DiscountForm
from django.shortcuts import redirect
from .models import User,Product,Order_Line,Cart
from .models import Category
from .models import ProductAndDiscountMemberShip, ProductDiscount
# for redirect
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib import messages

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
    all_items = Category.objects.all()
    return render(request, "categories.html", {'all_items': all_items})


def category(request,category_id):
    categName = Category.objects.get(pk=category_id)
    Products = Product.objects.filter(category=category_id)
    memberships = ProductAndDiscountMemberShip.objects.all()
    products_dict = dict((membership.product, membership.product_discount.discount_percent) for membership in list(memberships) if membership.product in Products)
    other_products = set(Products) - (products_dict.keys())
    other_products = dict((product, 'No Discount') for product in other_products)
    products_dict.update(other_products)
    return render(request, "category.html",{'category':categName.catName,'all_items': Products, 'products_dict': products_dict})

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
        catId=str(product.category.id)
        user = User.objects.get(pk=request.session['email'])
        try:
           cartid = Cart.objects.filter(User_em=request.session['email']).get(isCheckout=False)
        except :
            email = request.session['email']
            cartid=Cart()
            cartid.User_em=User.objects.get(pk=email)
            cartid.save()
        ol=Order_Line.objects.filter(CartId=cartid).filter(ProductID=product)
        if (ol):
            ol=Order_Line.objects.filter(CartId=cartid).get(ProductID=product)
            ol.Quantity=ol.Quantity+1
            ol.save()
        else :
            new_order=Order_Line()
            new_order.CartId=cartid
            new_order.ProductID=product
            new_order.price=product.price
            new_order.save()
    
        return redirect('../category/'+catId)
    else:
        return render(request, 'loggedin.html')


def delol(request,ol_id):
    if request.session.get('logged_in'):
        ol = Order_Line.objects.get(pk=ol_id)
        ol.delete()
        # messages.success(request, ('Item Has Been Deleted!'))
        return redirect('../cart/')
    else:
        return render(request, 'loggedin.html')

def forgotten_password(request):
    return render(request, 'forgotten_password.html')


def cart(request):
    
    if request.session.get('logged_in'):

        try:
           cartid = Cart.objects.filter(User_em=request.session['email']).get(isCheckout=False)
        except :
            email = request.session['email']
            cartid=Cart()
            cartid.User_em=User.objects.get(pk=email)
            cartid.save()

        ord_lin = Order_Line.objects.filter(CartId=cartid)
        totalprice=0
        for ol in ord_lin :
            totalprice += ol.Quantity * ol.price
        return render(request, 'cart.html', {'all_items': ord_lin,'total_price':totalprice})
    else:
        return render(request, 'home.html')

def buy(request):
    
    if request.session.get('logged_in'):
        
        email = request.session['email']
        old_cart = Cart.objects.filter(User_em=email).get(isCheckout=False)
        ord_lin = Order_Line.objects.filter(CartId=old_cart)
        totalprice=0
        for ol in ord_lin :
            totalprice += ol.Quantity * ol.price
        old_cart.total_price=totalprice
        old_cart.isCheckout=True
        old_cart.dt = datetime.datetime.now()
        old_cart.save()
        


        new_cart=Cart()
        new_cart.User_em=User.objects.get(pk=email)
        new_cart.save()

        return redirect('../cart/')
    else:
        return render(request, 'home.html')


def editqty(request,ol_id):

    if (request.session.get('logged_in') and request.method == 'POST'):
        edo = Editqtyform(request.POST)
        if(edo.is_valid()):
            
            quantity = edo.cleaned_data['quantity']

            ol = Order_Line.objects.get(pk=ol_id)
            ol.Quantity=quantity
            ol.save();
        else:
            print ('------------------------------else------------------------------')

        return redirect('../cart/')
    else:
        return render(request, 'home.html')

def history(request):

    if request.session.get('logged_in'):   
        title='this is history'
        carts = Cart.objects.filter(User_em=request.session['email']).filter(isCheckout=True)
        ols=[]
        for c in carts : 
            ol=Order_Line.objects.filter(CartId=c)
            ols.append((c,ol))
        ols.reverse()
        return render(request, 'history.html', {'title':title,'ols':ols})
    else:
        return render(request, 'home.html')



###################################ControlPanel Admin####################
def ControlPanel(request):
    if request.session.get('typ') == 'admin':
        return render(request, 'ControlPanel.html')
    else:
        return redirect('login')





def Adminprod(request):
    all_items=Product.objects.all()
    return render(request, 'AdminControl/Adminprod.html', {'all_items': all_items})

def adminEditP(request,products_ID):
    if request.method == 'POST':  
        product = Product.objects.get(pk=products_ID)
        form = ProductForm(request.POST or None, instance=product)
        if form.is_valid():
            form.save()
            cartid = Cart.objects.filter(User_em=request.session['email']).get(isCheckout=False)
            ord_lin = Order_Line.objects.filter(CartId=cartid)
            for order in ord_lin :
                order.price=form['price'].value()
                order.save()
            messages.success(request, (product.Name+' Has Been Edited!'))
            return redirect('.')
        else:
            print(form.errors.as_data())
            return render(request, 'AdminControl/Adminprod.html')
    else:
        product = Product.objects.get(pk=products_ID)
        Categories = Category.objects.values('catName')
        return render(request, 'AdminControl/Admineditprod.html', {'product': product,'Categories':Categories})



def adminaddP(request):
    if request.method == 'POST':
        product=Product()
        form = ProductForm(request.POST or None, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, (product.Name+' Has Been Added!'))
            return redirect('..')
        else:
            product.delete()
            print(form.errors.as_data())
            return redirect('..')
    else:
        Categories = Category.objects.values('catName')
        return render(request, 'AdminControl/AdminAddprod.html', {'Categories':Categories})


def adminDeletP(request,products_ID):
    product = Product.objects.get(pk=products_ID)
    product.delete()
    cartid = Cart.objects.filter(User_em=request.session['email']).get(isCheckout=False)
    ord_lin = Order_Line.objects.filter(CartId=cartid)
    for order in ord_lin :
        if order.ProductID.id==products_ID:
           del order
    messages.success(request, (product.Name+' Has Been Deleted!'))
    return  redirect('..')

def adminEditP(request,products_ID):
    if request.method == 'POST':  
        product = Product.objects.get(pk=products_ID)
        form = ProductForm(request.POST or None, instance=product)
        if form.is_valid():
            form.save()
            cartid = Cart.objects.filter(User_em=request.session['email']).get(isCheckout=False)
            ord_lin = Order_Line.objects.filter(CartId=cartid)
            for order in ord_lin :
                order.price=form['price'].value()
                order.save()
            messages.success(request, (product.Name+' Has Been Edited!'))
            return redirect('.')
        else:
            print(form.errors.as_data())
            return render(request, 'AdminControl/Adminprod.html')
    else:
        product = Product.objects.get(pk=products_ID)
        Categories = Category.objects.values('catName')
        return render(request, 'AdminControl/Admineditprod.html', {'product': product,'Categories':Categories})



def adminaddP(request):
    if request.method == 'POST':
        product=Product()
        form = ProductForm(request.POST or None, instance=product)
        print("Iam request.POST",request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, (product.Name+' Has Been Added!'))
            return redirect('..')
        else:
            #product.delete()
            print(form.errors.as_data())
            return redirect('..')
    else:
        #Categories = Category.objects.values('catName')
        Categories = Category.objects.all()
        return render(request, 'AdminControl/AdminAddprod.html', {'Categories':Categories})


def adminDeletP(request,products_ID):
    product = Product.objects.get(pk=products_ID)
    product.delete()
    cartid = Cart.objects.filter(User_em=request.session['email']).get(isCheckout=False)
    ord_lin = Order_Line.objects.filter(CartId=cartid)
    for order in ord_lin :
        if order.ProductID.id==products_ID:
           del order
    messages.success(request, (product.Name+' Has Been Deleted!'))
    return  redirect('..')



def Admincat(request):
    all_items = Category.objects.all()
    return render(request, 'AdminControl/Admincat.html', {'all_items': all_items})


def adminEditcat(request,Category_ID):
    print("Category_ID",Category_ID)
    Categories = Category.objects.values('catName')
    if request.method == 'POST':  
        category = Category.objects.get(pk=Category_ID)
        catName=category.catName
        print('category befor',category)
        form = CategoryForm(request.POST or None, instance=category)
        if form.is_valid():
           # catName2=form['catName'].value()

            form.save()
            print('category after',category)
            messages.success(request, (catName+' Has Been Edited!'))
            return  redirect('.')
        else:
            #print(form.errors.as_data())
            messages.success(request, (' this category is exists,try agin'))
            return redirect('.')
    else:        
        category = Category.objects.get(pk=Category_ID)
        return render(request, 'AdminControl/Admineditcat.html', {'category':category,'Categories':Categories})


def adminaddcat(request):
    if request.method == 'POST':  
        category = Category()
        form = CategoryForm(request.POST or None, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, (category.catName+' Has Been Added!'))
            return redirect('..')
        else:
           # print(form.errors.as_data())
            messages.success(request, (' this category is exists,try agin'))
            return redirect('.')
    else:
        
        Categories = Category.objects.values('catName')
        return render(request, 'AdminControl/AdminAddcat.html', {'Categories':Categories})


def Adminusers(request):
    users=User.objects.all()
    return render(request, 'AdminControl/Adminusers.html',{'users':users})



def adminEditUser(request,User_ID):
    user = User.objects.get(email=User_ID)
    if request.method == 'POST':  
        form = UserForm(request.POST or None, instance=user)
        if form.is_valid():

            form.save()
            messages.success(request, (str(user.email)+' Has Been Edited!'))
            return  redirect('.')
        else:
            #print(form.errors.as_data())
            messages.success(request, (' this user is exists,try agin'))
            return redirect('.')
    else:        
        return render(request, 'AdminControl/adminEditUser.html', {'user':user})


def adminadduser(request):
   if request.method == 'POST':
        #Get the posted form
        MySignupForm = SignUpForm(request.POST)
        if MySignupForm.is_valid():
            email = MySignupForm.cleaned_data['email']
            password = MySignupForm.cleaned_data['password']


            email_value = User.objects.filter(email=email).values()
            
            if(email_value):
                messages.success(request, (' this user is exists,try agin'))
                return redirect('.')

            new_user = User()
            new_user.email = email
            new_user.password = password
            new_user.save()
            c=Cart()
            c.User_em=new_user
            c.save()
            return redirect('..')

        else:
            #print(form.errors.as_data())
            messages.success(request, ('Error,try agin'))
            return redirect('.')
   else:        
        return render(request, 'AdminControl/AdminAdduser.html')

################## discounts views ##################
def discounts(request):
    discounts = ProductDiscount.objects.all()
    return render(request, 'AdminControl/Discounts.html',{'discounts':discounts})


def editDiscount(request, discount_id):
    # discountsM = ProductAndDiscountMemberShip.objects.values('id')
    if request.method == 'POST':  
        discount = ProductDiscount.objects.get(id=discount_id)
        form = DiscountForm(request.POST or None, instance = discount)
        if form.is_valid():
            title2 = form['title'].value()
            form.save()
            messages.success(request, (title2 +' Has Been Edited!'))
            return  redirect('.')
        else:
    #         #print(form.errors.as_data())
            messages.success(request, ('edit failed, try agin'))
            return redirect('.')
    else:       
        discount = ProductDiscount.objects.get(id=discount_id)
        return render(request, 'AdminControl/DiscountEdit.html', {'discount':discount})

def getProductsOfDiscount(discount_id):
    discountsM = ProductAndDiscountMemberShip.objects.filter(product_discount_id=discount_id)
    products = []
    for discountM in discountsM:
        products.append(discountM.product)
    return products

def updateDiscountProducts(request, discount_id):
    all_products = list(Product.objects.all())
    discount_products = getProductsOfDiscount(discount_id)
    other_products = list(set(all_products) - set(discount_products))
    discountsM = ProductAndDiscountMemberShip.objects.filter(product_discount_id=discount_id)

    if request.method == 'POST':  
        discount = ProductAndDiscountMemberShip.objects.get(id=discount_id)
        form = CategoryForm(request.POST or None, instance=discount)
        if form.is_valid():
            title2 = form['title'].value()
            discount_percent2 = form['discount_percent'].value()
            form.save()
            messages.success(request, (title2 +' Has Been Edited!'))
            return  redirect('.' + str(discount_id))
        else:
    #         #print(form.errors.as_data())
            messages.success(request, (' this discount is exists,try agin'))
            return redirect('.'+str(discount_id))
    else:       
        # discount = ProductAndDiscountMemberShip.objects.get(id=discount_id)
        return render(request, 'AdminControl/UpdateDiscountProducts.html', {'discountsM':discountsM,'discount_id':discount_id ,'all_products':all_products, 'discount_products': discount_products ,'other_products':other_products})


def deleteDiscountMemberShip(request, memberShip_id):
    discount_id = ProductAndDiscountMemberShip.objects.get(id=memberShip_id).product_discount.id
    if request.method == 'POST':  
        ProductAndDiscountMemberShip.objects.filter(id=memberShip_id).delete()
        messages.success(request, ('the product has been deleted from this discount'))
        return  redirect('/ControlPanel/Discounts/UpdateDiscountProducts' + str(discount_id))
    else:
        return  redirect('/ControlPanel/Discounts/UpdateDiscountProducts' + str(discount_id))

def addDiscountMemberShip(request, product_id, discount_id):
    if request.method == 'POST':  

        product = Product.objects.get(id=product_id)
        product_discount = ProductDiscount.objects.get(id=discount_id)
        discountM = ProductAndDiscountMemberShip(product=product, product_discount=product_discount)
        discountM.save()
        return  redirect('/ControlPanel/Discounts/UpdateDiscountProducts' + str(discount_id))
    else:
        discount = ProductDiscount.objects.get(id=discount_id)
        product = Product.objects.get(id=product_id)

        return render(request, 'AdminControl/addDiscountMemberShip.html', {'product': product ,'discount':discount})

def addDiscount(request):
    if request.method == 'POST':  
        productDiscount = ProductDiscount()
        form = DiscountForm(request.POST or None, instance=productDiscount)
        if form.is_valid():
            form.save()
            messages.success(request, (productDiscount.title+' Has Been Added!'))
            return redirect('..')
        else:
           # print(form.errors.as_data())
            messages.success(request, (' this discount is exists,try agin'))
            return redirect('.')
    else:
        return render(request, 'AdminControl/AdminAddDiscount.html')