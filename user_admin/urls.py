from django.urls import path
from user_admin import views

urlpatterns = [
  path('', views.home, name="home"),
  path('about/', views.about, name="about"),
  path('login/', views.login, name="login"),
  path('welcome/', views.welcome, name="welcome"),
  path('categories/', views.categories, name="categories"),
  path('signout/', views.signout, name="signout"),
  path('todo/', views.todo, name="todo"),

]