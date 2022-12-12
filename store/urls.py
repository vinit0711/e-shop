from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='homepage'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('cart', views.cart, name='cart'),
    path('check-out', views.checkout, name='checkout'),
    path('orders', views.orders, name='orders'),
    path('productpage/<int:pk>', views.productpage, name='productpage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
# student/<int:pk>/

htmxpattern = [
    path('check-email', views.check_email, name='check-email'),
]

urlpatterns += htmxpattern
