from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import User
from markdown2 import markdown
from . import util
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django import forms
import json
import smtplib
from email.message import EmailMessage
import ssl
# Create your views here.
class newBlog(forms.Form):
    title = forms.CharField(label= "Title", max_length=60)
    price = forms.IntegerField(label="Price")
    brand = forms.CharField(label="Brand", max_length=30)
    year = forms.IntegerField(label="Year")
    theModel = forms.CharField(label="Model", max_length=50)

@csrf_exempt
def brands(request):
   
    if request.method == "POST":
        data = json.loads(request.body)
        orderBlogs = []
        for blog in Blog.objects.all():
            if blog.car.brand in data["brands"]:
                orderBlogs.append(blog)
        orderBlogs.sort(key=lambda x: x.timestamp, reverse=True)
        orderBlogs_dict = {}
        orderBlogs_dict["length"] = len(orderBlogs)
        i = 0
        for blog in orderBlogs:
            temp = [blog.title, blog.car.brand, blog.car.year, blog.car.theModel]
            orderBlogs_dict[i] = temp
            i = i+1
        return JsonResponse(orderBlogs_dict, status=201)
        
        return HttpResponse('hello')
@csrf_exempt
def filter(request):
    if request.method == "POST":
        all_Brands = {}
        i = 0
        for car in Car.objects.all():
            x = car.brand in all_Brands.values()
            if (car.brand in all_Brands.values()) == False:
                all_Brands[i] = car.brand
                i = i+1 
        length = len(all_Brands)
        all_Brands["Length"] = length
        return JsonResponse(all_Brands, status=201)
    else:
        return HttpResponse("Not a Page")
def request(request):
    if request.method == "POST":
        comment = request.POST["content"]
        email_password = "zfsyzsoezezluqyl"
        msg = EmailMessage()
        msg['From'] = "hello.carblog@gmail.com"
        msg['Subject'] = "Blog Request"
        if request.user.is_authenticated:
            msg['To'] = ["hello.carblog@gmail.com", request.user.email]
        else:
            msg['To'] = "hello.carblog@gmail.com"
        msg.set_content(comment)
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login("hello.carblog@gmail.com", email_password)
                smtp.sendmail("hello.carblog@gmail.com","hello.carblog@gmail.com", msg.as_string()) 
                return render(request,"carblog/request.html", {
                "message": "email sucess"
            })
    else:
        return render(request, "carblog/request.html")



    return render(request,"carblog/request.html")
def create(request):
    if request.user.is_superuser:
        if request.method == "POST":
            m_content = request.POST.get('content')
            title = request.POST["title"]
            price = request.POST["price"]
            brand = request.POST["brand"]
            year = request.POST["year"]
            theModel = request.POST["theModel"]
            
            #testing 
            for entry in util.list_entries():
                if title.replace(" ","-") == entry:
                    return render(request,"carblog/create.html",{
                        "message": "Error: title is already taken",
                        "newBlogForm": newBlog()
                    })
            #creating markdown page
            util.save_entry(title.replace(" ","-"),m_content)

            c = Car(price=price,brand=brand,year=year,theModel=theModel)
            c.save()
            blog = Blog(title=title,car=c)
            blog.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "carblog/create.html",{
                "newBlogForm": newBlog()
            })
    else:
        return HttpResponse("must be a superuser to access this page")
    

@login_required
def page(request, title):
    markPage = markdown(util.get_entry(title))
    if markPage == None:
        return HttpResponse("uh oh, something went wrong on our side")
    
    return render(request,"carblog/page.html",{
        "markPage": markPage
    })
    """return render(request, "carblog/page.html")"""

@csrf_exempt
def allposts(request):
    if request.method == "POST":
        orderBlogs = []
        for blog in Blog.objects.all():
            orderBlogs.append(blog)
        orderBlogs.sort(key=lambda x: x.timestamp, reverse=True)
        orderBlogs_dict = {}
        orderBlogs_dict["length"] = len(orderBlogs)
        i = 0
        for blog in orderBlogs:
            temp = [blog.title, blog.car.brand, blog.car.year, blog.car.theModel]
            orderBlogs_dict[i] = temp
            i = i+1
        
        return JsonResponse(orderBlogs_dict, status=201)
    
    return render(request, "carblog/allPosts.html")

def index(request):
    return render(request, "carblog/about.html")

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
            return render(request, "carblog/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "carblog/login.html")


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
            return render(request, "carblog/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "carblog/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "carblog/register.html")

