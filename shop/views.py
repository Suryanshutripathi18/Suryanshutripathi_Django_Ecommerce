from django.shortcuts import render, redirect
from .models import  Product, Contact, Orders
from math import ceil
import json
from django.contrib.auth.decorators import login_required



# Create your views here.
from django.http import HttpResponse, response

login_required(login_url='/shop/login')
def index(request):


    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        
        allProds.append([prod, 4])

    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

login_required(login_url='/shop/login')
def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
        return False

login_required(login_url='/shop/login')
def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        
        if len(prod) != 0:
            allProds.append([prod, range ])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<=2:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


login_required(login_url='/shop/login')
def contact(request):
    thank=False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
      
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank=True
    return render(request, 'shop/contact.html', {'thank':thank})


login_required(login_url='/shop/login')
def productView(request, myid):

    product = Product.objects.filter(id = myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})

login_required(login_url='/shop/login')
def checkout(request):
    
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        amount= request.POST.get('amount', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')

        order = Orders(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        thank=True
      
        id=order.order_id
     
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})

      

    return render(request, 'shop/checkout.html')

from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.

def login_page(request):
        
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')


            if not User.objects.filter(username = username).exists():
                messages.error(request , 'Invalid Username')
                return redirect('/shop/login_page/')
                  
            
            user = authenticate(username = username , password = password)

            if user is None:
                messages.error(request , 'Invalid Password')
                return redirect('/shop/login_page/')
            
            else :
                login(request,user)
                return redirect('/shop/')

          


        return render(request,'shop/login.html') 


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request,'Username already taken')
            return redirect("/shop/register/")
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save()

        messages.info(request,'Account created successfully!')


        return redirect('/shop/')

        
    return render(request,'shop/register.html') 


def logout_page(request):
    logout(request)
    return redirect("/shop/register_page/")

