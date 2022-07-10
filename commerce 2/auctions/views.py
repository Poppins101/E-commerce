from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Product, Comment, Bid, Watchlist 


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("listings"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')   
def create(request):
    if request.method == "POST": 
        user = request.user
        date = request.POST['date_listed']
        image =request.FILES['image']
        products = Product.objects.create(user=user, title=request.POST['title'], price=request.POST['price'], description=request.POST['description'], image=image, date=date)
        products.save()
        
        return HttpResponseRedirect(reverse("listings"))
    else:
        return render(request, 'auctions/create.html')    


def listings(request):
    products = Product.objects.all() 
    return render(request, 'auctions/listings.html',{
        'products':products
    })

@login_required(login_url='login')
def bid(request, name):
    if request.method == "POST":
        user = request.user
        bid = request.POST['bid']
        bids = Bid.objects.create(user=user, bid=bid)
        product = Product.objects.get(title=name)
        bids.save()
        bids.product.add(product)
        return HttpResponseRedirect(reverse("listings"))
        
    product= Product.objects.get(title=name)
    total_bids = Bid.objects.all()
    bid_num = 0
    for bids in total_bids:
        bid_num+=1
    return render(request, "auctions/bid.html",{
        "product": product,
        "bids":bid_num,
        
    })

