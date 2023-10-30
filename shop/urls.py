
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("contact/", views.contact, name="ContactUs"),
    path("products/<int:myid>", views.productView, name="Productview"),
    path("checkout/", views.checkout, name="Checkout"),
    path("search/", views.search, name="Search"),
    path("login_page/", views.login_page , name='login_page'),
    path("register_page/" , views.register_page , name='register_page'),
    path("logout_page/" , views.logout_page , name='logout_page'),
    
   

]