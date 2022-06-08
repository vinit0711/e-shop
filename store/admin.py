from django.contrib import admin
from .models.products import Product
from .models.category import Category 
from .models.customer import Customer

# Register your models here.

@admin.register(Product)
class Product (admin.ModelAdmin):
    list_display = ['name','category','price','description','image']

@admin.register(Category)
class Category (admin.ModelAdmin):
    list_display =['name','description']

@admin.register(Customer)
class Customer (admin.ModelAdmin):
    list_display = ['first_name','last_name','phone_number','email','password']