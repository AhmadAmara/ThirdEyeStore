from django import forms  
from .models import Product

class StudentForm(forms.Form):  
    firstname = forms.CharField(label="Enter first name",max_length=50)  
    lastname  = forms.CharField(label="Enter last name", max_length = 10)  
    email     = forms.EmailField(label="Enter Email")  
    file      = forms.FileField() # for creating file input  
    
    
class LoginForm(forms.Form):
   email    = forms.EmailField(label="Enter Email") 
   password = forms.CharField(widget = forms.PasswordInput())


class SignUpForm(forms.Form):
   email = forms.CharField(max_length = 100)
   password = forms.CharField(widget = forms.PasswordInput())
  

class Order(forms.Form):
   ProdectID = forms.CharField(label="ProductID",max_length = 100)
  
#class ProductForm(forms.ModelForm):
    #	class Meta:
		#model = Product
	#	fields= ["product", "completed"]

