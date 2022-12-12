from django.db import models
from django.shortcuts import get_object_or_404
from django.http import Http404


class Customer (models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def emailcheck(self):
        return Customer.objects.filter(email=self.email)

    def getcustomer(email):
        print("email==", email)
        # customer = get_object_or_404(Customer, email=email)
        # print("Customer==", customer)
        try:
            return Customer.objects.get(email=email)
        except:
            raise Http404("Customer Does Not Exist")
