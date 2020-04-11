from django import forms  
from .models import Product
from .models import Category
from .models import User, ProductDiscount, ProductAndDiscountMemberShip

class StudentForm(forms.Form):  
    firstname = forms.CharField(label="Enter first name",max_length=50)  
    lastname  = forms.CharField(label="Enter last name", max_length = 10)  
    email     = forms.EmailField(label="Enter Email")  
    file      = forms.FileField() # for creating file input  
    
    
class LoginForm(forms.Form):
   email    = forms.EmailField(label="Enter Email") 
   password = forms.CharField(widget = forms.PasswordInput())


class SignUpForm(forms.Form):
   email =  forms.EmailField(label="Enter Email") 
   password = forms.CharField(widget = forms.PasswordInput())


class Editqtyform(forms.Form):
   quantity = forms.IntegerField()

class ProductForm(forms.ModelForm):
   class Meta:
      model = Product
      fields= ["category", "Name","Weight","price","Quantity"]

class CategoryForm(forms.ModelForm):
   class Meta:
      model = Category
      fields= ["catName", "isAvtive"]

class DiscountForm(forms.ModelForm):
   class Meta:
      model = ProductDiscount
      fields = ["title", "discount_percent"]

class DiscountMemberShipForm(forms.ModelForm):
   class Meta:
      model = ProductAndDiscountMemberShip
      fields = ["product", "product_discount", "end_date"]

class UserForm(forms.ModelForm):
   class Meta:
      model = User
      fields= ["password", "typ"]
