from django.contrib import admin

# Register your models here.

from .models import User
admin.site.register(User)
from .models import Product
admin.site.register(Product)

from .models import Category
admin.site.register(Category)
