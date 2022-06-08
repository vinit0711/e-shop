from django.db import models


class Customer (models.Model):
    first_name =models.CharField(max_length=100)
    last_name =models.CharField(max_length=50)
    phone_number=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=500)

    def emailcheck(self):
        return Customer.objects.filter(email=self.email)

    def getcustomer(email):
        return Customer.objects.get(email=email)