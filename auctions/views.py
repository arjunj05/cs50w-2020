from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bids, Watchlist, Comment

class createListingForm(forms.Form):
    title = forms.CharField(label="title", max_length=30)
    description = forms.CharField(label="description", max_length=200)
    price = forms.IntegerField(label="price")
    imageURL = forms.CharField(label="imageURL", max_length=400, required = False)
    category = forms.CharField(label="category", max_length=20, required = False)

class newBid(forms.Form):
    bid = forms.IntegerField(label="bid")

def index(request):
    return render(request, "auctions/index.html", {
        "lists": Listing.objects.filter(isActive=True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
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
    
@login_required
def create(request):
    if request.method == "POST":
        tit = request.POST["title"]
        des = request.POST["description"]
        pr = request.POST["price"]
        imgURL = request.POST["imageURL"]
        cat = request.POST["category"]
        l = Listing(title=tit, description=des, price=pr,imageURL=imgURL, category=cat, isActive=True, user=request.user)
        l.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request,"auctions/create.html", {
        "form": createListingForm()
    })
@login_required
def listing(request, lID):
    x = False
    for watcher in Watchlist.objects.filter(listing_id=lID):
        if request.user == watcher.user:
            x = True
    if request.method == "POST":
        bid = int(request.POST["bid"])
        l = Listing.objects.get(id=lID)
        if bid > int(l.price):
            u = request.user
            b = Bids(user=u, listing=l, price=bid)
            b.save()
            l.price = bid
            l.save()
        else:
            return render(request, "auctions/listing.html", {
                "toLow": True, "form1": newBid(), "listObj": Listing.objects.get(id=lID),
                "inWatchList": x,
                "Comments": Comment.objects.filter(listing=Listing.objects.get(id=lID))
            })
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/listing.html", {
        "listObj": Listing.objects.get(id=lID), 
        "form1": newBid(),
        "inWatchList": x,
        "Comments": Comment.objects.filter(listing=Listing.objects.get(id=lID))
    })
def categories(request):
    catSet = set()
    for cat in Listing.objects.filter(isActive=True):
        if cat.category != "":
            catSet.add(cat.category)
    return render(request, "auctions/categories.html", {
        "catList": catSet,
        "allListings": Listing.objects.all()
    })
def category_list(request, cat):
    l = Listing.objects.filter(category=cat)
    return render(request, "auctions/catList.html", {
        "objs": l 
    })
def watchlist(request, lID):
    x = False
    for watcher in Watchlist.objects.filter(listing_id=lID):
        if request.user == watcher.user:
            x = True

    if x:
        for watcher in Watchlist.objects.filter(listing_id=lID):
            if request.user == watcher.user:
                watcher.delete()
                x = False
    else:
        x = Watchlist(user=request.user, listing=Listing.objects.get(id=lID))
        x.save()
        x = True
    return render(request, "auctions/listing.html", {
        "listObj": Listing.objects.get(id=lID), 
        "form1": newBid(),
        "inWatchList": x,
        "Comments": Comment.objects.filter(listing=Listing.objects.get(id=lID))
    })
def watchlist_list(request):
    watchlist_listings = Watchlist.objects.filter(user_id=request.user.id)
    objes =[]
    for x in watchlist_listings:
        if x.listing.isActive:
            objes.append(x.listing)
    return render(request,"auctions/catlist.html", {
        "objs": objes
    })
def endbid(request, lID):
    if request.method == "POST":
        x = Listing.objects.get(id=lID)
        x.isActive =False
        x.save()
        return HttpResponseRedirect(reverse("index"))

def past_listings(request):
    # create variable with all the unactive lsitings
    x = Listing.objects.filter(isActive=False)
    return render(request, "auctions/pastListings.html", {
        "objs": x
    })
def pastList(request,lID):
    l = Listing.objects.get(id=lID)
    y = 0
    for x in Bids.objects.filter(listing=l):
        if x.price == l.price:
            return render(request, "auctions/pastList.html", {
                "soldFor": x.price,
                "winner": x.user
            })

    return HttpResponse("for loop didnt work lmao")
def comment(request,lID):
    m = request.POST["comment"]
    c = Comment(message=m, user=request.user, listing=Listing.objects.get(id=lID))
    c.save()
    return HttpResponseRedirect(reverse('listing', kwargs={'lID':lID}))


