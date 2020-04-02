from django.contrib import admin

# Register your models here.
from .models import List
admin.site.register(List)

from .models import User
admin.site.register(User)