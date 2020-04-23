from django.urls import path
from user_admin import views

urlpatterns = [
  path('', views.home, name="home"),
  path('about/', views.about, name="about"),
  path('login/', views.login, name="login"),
  path('welcome/', views.welcome, name="welcome"),
  path('cart/', views.cart, name="cart"),
  path('history/', views.history, name="history"),
  path('categories/', views.categories, name="categories"),
  path('signup/', views.signup, name="signup"),
  path('category/<category_id>', views.category, name="category"),
  # path('category/<category_id>/<product_id>', views.ShowProduct, name="ShowProduct"),
  path('addorder/<Product_id>', views.addorder, name="addorder"),
  path('delol/<ol_id>', views.delol, name="delol"),
  path('buy/', views.buy, name="buy"),
  path('editqty/<ol_id>', views.editqty, name="editqty"),
  path('signout/', views.signout, name="signout"),
  path('ControlPanel/', views.ControlPanel, name="ControlPanel"),
  path('ControlPanel/Categories/', views.Admincat, name="Admincat"),
  path('ControlPanel/Categories/<Category_ID>', views.adminEditcat, name="adminEditcat"),
  path('ControlPanel/Categories/add/', views.adminaddcat, name="adminaddcat"),
  path('ControlPanel/Products/', views.Adminprod, name="Adminprod"),
  path('ControlPanel/Users/', views.Adminusers, name="Adminusers"),
  path('ControlPanel/Users/<User_ID>', views.adminEditUser, name="adminEditUser"),
  path('ControlPanel/Users/add/', views.adminadduser, name="adminadduser"),
  path('ControlPanel/Products/<products_ID>', views.adminEditP, name="adminEditP"),
  path('ControlPanel/Products/Delet/<products_ID>', views.adminDeletP, name="adminDeletP"),
  path('ControlPanel/Products/add/', views.adminaddP, name="adminaddP"),
  path('forgotten_password/', views.forgotten_password, name="forgotten_password"),

  path('ControlPanel/Discounts/', views.discounts, name="Discounts"),
  path('ControlPanel/Discounts/DiscountEdit<discount_id>', views.editDiscount, name="editDiscount"),
  path('ControlPanel/Discounts/UpdateDiscountProducts/<discount_id>', views.updateDiscountProducts, name="updateDiscountProducts"),
  path('ControlPanel/Discounts/UpdateDiscountProducts/delete/<memberShip_id>', views.deleteDiscountMemberShip, name="deleteDiscountMemberShip"),
  path('ControlPanel/Discounts/UpdateDiscountProducts/add/<product_id><discount_id>', views.addDiscountMemberShip, name="addDiscountMemberShip"),
  path('ControlPanel/Discounts/add/', views.addDiscount, name="addDiscount"),
  path('ControlPanel/Discounts/delete/<discount_id>', views.deleteDiscount, name="deleteDiscount"),


]


  ##path('ControlPanel/Categories/Delet/<Category_ID>', views.adminDeletcat, name="adminDeletcat"),
  ###