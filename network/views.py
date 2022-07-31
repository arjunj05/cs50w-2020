from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.decorators.csrf import csrf_exempt


class createNewTweet(forms.Form):
    content = forms.CharField(label="content", max_length="280")

@csrf_exempt
def loadLike(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("postId")
        postObj = Post.objects.get(id=post_id)
        hasLiked = False
        numLikes = Like.objects.filter(likedPost=postObj).count() 
        for likedObj in Like.objects.filter(likedPost=postObj):
            if likedObj.liker == request.user:
                hasLiked = True
        print(hasLiked)
        return JsonResponse({"hasLiked": hasLiked, "numLikes": numLikes}, status=201)
    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = data.get("postId")
        postObj = Post.objects.get(id=post_id)
        hasLiked = data.get("hasLiked")
        if hasLiked:
            x = Like.objects.get(likedPost=postObj, liker=request.user)
            x.delete()
        else:
            x = Like(likedPost=postObj, liker=request.user)
            x.save()
        return JsonResponse({"message": "Post updated successfully."}, status=201)


@csrf_exempt
def like(request):
    data = json.loads(request.body)
    post_id = data.get("postId")

    thePost = Post.objects.get(id=post_id)

    likedObjs = Like.objects.filter(likedPost=thePost)
    likerList = []

    for x in likedObjs:
        likerList.append(x.liker)
    if( request.user in likerList ):
        y = Like.objects.get(liker=request.user, likedPost=thePost)
        y.delete()
    else:
        y = Like(liker=request.user, likedPost=thePost)
        y.save()
    return JsonResponse({"message": "Post updated successfully."}, status=201)


@csrf_exempt
def update(request):
    data = json.loads(request.body)
    post_id = data.get("postId")
    post_content = data.get("postContent")

    print(post_id)
    print(post_content)


    if Post.objects.get(id=post_id).user == request.user:
        print('check 2')
        x = Post.objects.get(id=post_id)
        x.body = post_content
        x.save()

    if request.method == "POST":
        return JsonResponse({"message": "Post updated successfully."}, status=201)

def index(request):
    if request.method == "POST":
        x = Post(user=request.user, body=request.POST["content"])
        x.save()
    posts = Post.objects.all()
    orderPosts = posts.order_by("-timestamp").all()

    post_paginator = Paginator(orderPosts, 10)
    page_num = request.GET.get('page')
    
    page = post_paginator.get_page(page_num)

    return render(request, "network/index.html",{
        "postForm": createNewTweet(),
        "page": page,
        "allLikes": Like.objects.all()
    })

def profile(request, profiler):
    profileUser = User.objects.get(username=profiler)
    isFollowing = None 
    x = Following.objects.filter(following=profileUser,follower=request.user)
    posts = Post.objects.filter(user=profileUser)
    if request.method == "POST":
        if x.count() >0:
            x.delete()
            isFollowing = False 
        else:
            y = Following(following=profileUser, follower=request.user)
            y.save()
            isFollowing = True
    else:
        if x.count() > 0:
            isFollowing =True
        else:
            isFollowing = False
    orderPosts = posts.order_by("-timestamp").all()
    post_paginator = Paginator(orderPosts, 10)
    page_num = request.GET.get('page')
    
    page = post_paginator.get_page(page_num)

    return render(request, "network/profile.html", {
            "isFollowing": isFollowing,
            "numFollowing": Following.objects.filter(follower=profileUser).count(),
            "numFollowers": Following.objects.filter(following=profileUser).count(),
            "page": page,
            "profiler": profileUser,
            "allLikes": Like.objects.all()
        })
def following(request): 
    followingObjs = Following.objects.filter(follower=request.user)
    orderPosts = []
    for followingObj in followingObjs:
        user = followingObj.following
        userPosts = Post.objects.filter(user=user)
        for post in userPosts:
            orderPosts.append(post)

    orderPosts.sort(key=lambda x: x.timestamp, reverse=True)

    post_paginator = Paginator(orderPosts, 10)
    page_num = request.GET.get('page')
    
    page = post_paginator.get_page(page_num)
    return render(request, "network/following.html", {
        "page": page,
        "allLikes": Like.objects.all()
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
