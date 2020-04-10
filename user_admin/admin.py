from django.contrib import admin

# Register your models here.

from .models import User
admin.site.register(User)

from .models import Product
admin.site.register(Product)

from .models import Category
admin.site.register(Category)

from .models import Order_Line
admin.site.register(Order_Line)

from .models import Cart
admin.site.register(Cart)

from .models import PackgeSale
admin.site.register(PackgeSale)

from .models import ProductAndPackgeMemberShip
admin.site.register(ProductAndPackgeMemberShip)

from .models import ProductDiscount
admin.site.register(ProductDiscount)

from .models import ProductAndDiscountMemberShip
admin.site.register(ProductAndDiscountMemberShip)