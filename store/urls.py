from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home , name='homepage'),
    path('signup',views.signup , name='signup'),
    path('login',views.login , name='login'),
    path('logout',views.logout , name='logout'),
    path('cart',views.cart , name='cart'),
    path('check-out',views.checkout , name='checkout'),
    path('orders',views.orders , name='orders'),
    path('productpage/<int:pk>',views.productpage , name='productpage'),
]
#student/<int:pk>/