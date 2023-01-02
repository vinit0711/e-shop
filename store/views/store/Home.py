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


class Home(View):
    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart')
        customer = request.session.get('customer')
        if not customer:
            return redirect('login')
        if not cart:
            request.session.cart = {}   # adding cart in session if not already created
        products = None     # initialised  products as None
        categories = Category.get_all_category()
        # print(request.GET)
        categoryid = request.GET.get('category')
        page = request.GET.get('page', 1)

        if categoryid:
            products = Product.get_all_product_by_categoryid(categoryid)
        else:
            products = Product.get_all_products()
        paginator = Paginator(products, 2)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        # for page in range(1, paginator.num_pages + 1):
        context = {'products': products,
                   'categories': categories, 'customer': customer, 'Vinit': 'Mayurs', 'page_obj': page_obj}
        print(" you are in home page , user email==  :  ",
              request.session.get('email'))
        return render(request, 'Home.html', context)

    def post(self, request, *args, **kwargs):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        customer = request.session.get('customer')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart is :', cart)
        print(" you are in home post :  ", request.session.get('email'))
        return redirect("homepage")
