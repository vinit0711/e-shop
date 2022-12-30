from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models.products import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from django.contrib.auth.hashers import make_password, check_password
from store.middlewares.auth import auth_middleware

from .forms import CustomerForm


def logout(request):
    request.session.clear()
    return redirect('login')


def cart(request):
    products = []
    # for key, value in request.session.items():
    #     print('{} => {}'.format(key, value))
    customer = request.session.get('customer')
    print("received customer")
    if request.session.get('cart'):
        print("here")
        ids = list(request.session.get('cart').keys())
        products = Product.get_all_products_by_id(ids)
        # print(products)
        # print("you are in cart :", customer)
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
