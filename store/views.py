from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models.products import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from django.contrib.auth.hashers import make_password, check_password
from store.middlewares.auth import auth_middleware

from .forms import CustomerForm


def home(request):
    if request.method == 'GET':
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
        if categoryid:
            products = Product.get_all_product_by_categoryid(categoryid)
        else:
            products = Product.get_all_products()
        context = {'products': products,
                   'categories': categories, 'customer': customer, 'Vinit': 'Mayurs'}
        print(" you are in home page , user email==  :  ",
              request.session.get('email'))
        return render(request, 'Home.html', context)
    else:
        # Post request
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


def validate_customer(customer):
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


def registerUser(request):  # function handling post request of sign up
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

    error_message = validate_customer(customer)

    # Form Saving

    if not error_message:
        # before storing in database , hasing of password
        customer.password = make_password(customer.password)
        customer.save()  # saving customer object in database
        return redirect("homepage")
    else:
        print(error_message)
        # Prefilled fields if any error occur does not disappear
        # setting value attribute in html
        context = {'first_name': first_name, 'last_name': last_name,
                   'phone_number': phone_number, 'email': email, 'password': password, 'error_message': error_message}
        return render(request, "signup.html", context)


def signup(request):

    if request.method == 'GET':
        return render(request, "signup.html")
    else:   # post request
        return registerUser(request)


def login(request):
    if request.method == 'GET':
        print("login Get form")
        customer_form = CustomerForm()
        # print(customer_form)
        context = {'customer_form': customer_form}
        return render(request, "login.html", context)
    else:  # Post Request
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


def logout(request):
    request.session.clear()
    return redirect('login')


def cart(request):

    ids = list(request.session.get('cart').keys())
    customer = request.session.get('customer')
    products = Product.get_all_products_by_id(ids)
    # print(products)
    print("you are in cart :", customer)
    return render(request, 'cart.html', {'products': products, 'customer': customer})


def checkout(request):
    customer = request.session.get('customer')
    print("you are in check out  :", customer)
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')

        product = list(cart.keys())    # getting list of all products
        # this will show all products by ids in cart
        products = Product.get_all_products_by_id(product)
        print(address, phone, customer, cart, products)

        for product in products:    # creating order object
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
# str prroduct id was taken bcoz product.id was integer and in dictionary we needed string
            order.save()
            print("your order is : ", order)
            request.session['cart'] = {}   # clearing the cart
        return redirect("cart")


@auth_middleware
def orders(request):
    customer = request.session.get('customer')
    orders = Order.get_orders_by_customer(customer)
    print(orders)
    print("orders===", orders)
    return render(request, "orders.html", {'orders': orders})


def productpage(request, pk):

    product = Product.get_product_info_by_id(pk)
    product = Product.objects.get(id=pk)
    print(product.name)
    return render(request, "product.html", {'product': product})


def check_email(request):
    email = request.POST.get('email')
    if Customer.objects.filter(email=email).exists():
        return HttpResponse("<div style = 'color:red'> Email is already in use</div>")
    else:
        return HttpResponse("<div style = 'color:green'> Email is available</div>")


def check_phone_number(request):
    phone_number = request.POST.get('phone_number')
    if Customer.objects.filter(phone_number=phone_number).exists():
        return HttpResponse("<div style = 'color:red'> Phone Number is Already Registered</div>")
    # else:
    #     return HttpResponse("<div style = 'color:green'> Email is available</div>")


def cart_item_length(cart):
    if cart:
        return len(cart)
    else:
        return 0


def add_product_to_cart(request, pk):
    product = str(pk)
    print("product===", product)
    remove = request.POST.get('remove')
    print("remove===", remove)
    cart = request.session.get('cart')
    print("cart==", cart)
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
    else:  # Initially cart is empty , create cart obj and add to session
        cart = {}
        cart[product] = 1

    request.session['cart'] = cart
    print('cart is :', cart)
    print(" add_product_to_cart :  ", request.session.get('email'))
    # return redirect("homepage")
    categoryid = request.GET.get('category')
    if categoryid:
        products = Product.get_all_product_by_categoryid(categoryid)
    else:
        products = Product.get_all_products()
    cart_quantity = cart_item_length(cart)
    context = {'products': products, 'cart_quantity': cart_quantity}
    return render(request, "components/products.html", context)
