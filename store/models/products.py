from django.db import models
from .category import Category

class Product(models.Model):
   
    name=models.CharField(max_length=250)
    category=models.ForeignKey(Category , on_delete=models.CASCADE)
    price=models.IntegerField(default=0)
    description=models.CharField(max_length=250 ,null=True , default='')
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.name

    @staticmethod

    def get_all_products_by_id(ids):
        
        return Product.objects.filter(id__in = ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_all_product_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            Product.get_all_products()

    @staticmethod
    def get_product_info_by_id(id):
        if id:
            return  Product.objects.filter(id = id)
        else:
            pass