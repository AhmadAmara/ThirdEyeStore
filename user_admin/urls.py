from django.urls import path
from user_admin import views

urlpatterns = [
  path('', views.home, name="home"),
  path('about/', views.about, name="about"),
  path('login/', views.login, name="login"),
  path('welcome/', views.welcome, name="welcome"),
  path('cart/', views.cart, name="cart"),
  path('categories/', views.categories, name="categories"),
  path('signup/', views.signup, name="signup"),
  path('category/<category_id>', views.category, name="category"),
  path('addorder/<Product_id>', views.addorder, name="addorder"),
  path('signout/', views.signout, name="signout"),
  path('forgotten_password/', views.forgotten_password, name="forgotten_password")

]