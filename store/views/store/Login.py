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


class Login(View):
    def get(self, request, *args, **kwargs):
        print("login Get form")
        customer_form = CustomerForm()
        # print(customer_form)
        context = {'customer_form': customer_form}
        return render(request, "login.html", context)
        # return render(request, 'Home.html', context)

    def post(self, request, *args, **kwargs):
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            customer = Customer.getcustomer(email)
            error_message = None
            if customer:
                flag = check_password(password, customer.password)
                if flag:
                    # adding values in session
                    request.session['customer'] = customer.id
                    request.session['email'] = customer.email
                    return redirect("homepage")
                else:
                    error_message = "Invalid username or password"

            else:
                error_message = "Invalid username or password"

            return render(request, "login.html", {'error_message': error_message})
        except Exception as e:
            print("exception ===", str(e))
            error_message = "Invalid username or password"
            return render(request, "login.html", {'error_message': error_message})
