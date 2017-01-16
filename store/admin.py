from django.contrib import admin
from .models import Category, Staff, Comment, Order

admin.site.register(Category)
admin.site.register(Staff)
admin.site.register(Comment)
admin.site.register(Order)

# Register your models here.
