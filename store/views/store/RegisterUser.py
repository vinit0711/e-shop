from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from store.models.products import Product
from store.models.category import Category
from store.models.customer import Customer
from store.models.orders import Order
from django.contrib.auth.hashers import make_password, check_password
from store.middlewares.auth import auth_middleware
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from store.forms import CustomerForm
from django.contrib import messages


class RegisterUser(View):
    def get(self, request, *args, **kwargs):
        return render(request, "signup.html")

    def post(self, request, *args, **kwargs):
        return self.registerUser(request)

    def registerUser(self, request):  # function handling post request of sign up
        # return HttpResponse ("post Request")
        # corresponds to field "name" in html template
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone_number = request.POST.get('phonenumber')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Creating new customer object of Class customer
        customer = Customer(first_name=first_name, last_name=last_name,
                            phone_number=phone_number, email=email, password=password)

        error_message = self.validate_customer(customer)

        # Form Saving

        if not error_message:
            # before storing in database , hasing of password
            customer.password = make_password(customer.password)
            customer.save()  # saving customer object in database
            messages.success(
                request, "Account created for user  " + first_name + " " + last_name)
            return redirect("homepage")
        else:
            print(error_message)
            # Prefilled fields if any error occur does not disappear
            # setting value attribute in html
            context = {'first_name': first_name, 'last_name': last_name,
                       'phone_number': phone_number, 'email': email, 'password': password, 'error_message': error_message}
            return render(request, "signup.html", context)

    def validate_customer(self, customer):
        error_message = None

        if (not customer.first_name):
            error_message = "First name Required !"
        elif len(customer.first_name) < 4:
            error_message = "First name too short !"
        elif (not customer.last_name):
            error_message = "last name Required !"
        elif len(customer.last_name) < 3:
            error_message = "last name too short !"
        elif (not customer.phone_number):
            error_message = "Phone number Required !"
        elif len(customer.phone_number) < 10:
            error_message = "Phone number 10 digits required !"
        elif (not customer.email):
            error_message = "email Required !"
        elif len(customer.email) < 4:
            error_message = "emaail atleast 4 charac required !"
        elif customer.emailcheck():
            error_message = "Email Already present"

        return error_message
