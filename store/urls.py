from django.contrib import admin
from django.urls import path
from . import globalviews as views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from store.views.store import Home, Login, RegisterUser

urlpatterns = [
    path('', Home.Home.as_view(), name='homepage'),
    path('signup', RegisterUser.RegisterUser.as_view(), name='signup'),
    path('login', Login.Login.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('cart', views.cart, name='cart'),
    path('check-out', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('productpage/<int:pk>', views.productpage, name='productpage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

htmxpattern = [
    path('check-email', views.check_email, name='check-email'),
    path('add_product_to_cart/<int:pk>', views.add_product_to_cart,
         name='add_product_to_cart')
]

urlpatterns += htmxpattern
