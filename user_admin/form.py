from django import forms  
from .models import Product
from .models import Category
from .models import User, ProductDiscount, ProductAndDiscountMemberShip

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
      fields= ["category", "Name","Weight","price","Quantity","Image"]

class CategoryForm(forms.ModelForm):
   class Meta:
      model = Category
      fields= [ "isAvtive","catName","Image"]

class DiscountForm(forms.ModelForm):
   class Meta:
      model = ProductDiscount
      fields = ["title", "discount_percent"]

class DiscountMemberShipForm(forms.ModelForm):
   class Meta:
      model = ProductAndDiscountMemberShip
      fields = ["product", "product_discount"]

class UserForm(forms.ModelForm):
   class Meta:
      model = User
      fields= ["password", "typ"]
