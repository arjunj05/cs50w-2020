from django.shortcuts import render
from django.http import HttpResponse
from . import util
import numpy  
from numpy import random
from django import forms
from markdown2 import markdown
from django.urls import reverse
from django.http import HttpResponseRedirect


class NewTaskForm(forms.Form):
    task = forms.CharField(label= "someInput")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def page(request, name):
        if util.get_entry(name) == None:
            return render(request,"encyclopedia/errorPage.html")
        return render(request, "encyclopedia/page.html", {
        "markPage": markdown(util.get_entry(name)), "markName": name
        })

def randomPage(request):
    allEnteries = util.list_entries()
    x = random.randint(0,len(allEnteries)-1)
    return render(request, "encyclopedia/page.html", {
    "markPage": markdown(util.get_entry(allEnteries[x])), "markName": allEnteries[x]
    })

def search(request): 
    sReq = request.GET.get('s')
    print(request.GET.get('s'))
    if util.get_entry(sReq) != None:
        return render(request, "encyclopedia/page.html", {
        "markPage": markdown(util.get_entry(sReq)), "markName": sReq
        })
    else:
        allEnteries = util.list_entries()
        resultSet = set()
        for entry in allEnteries:
            if len(sReq) < len(entry):
                for i in range(0,len(entry)-len(sReq) +1):
                    if sReq == entry[i : i+len(sReq)]:
                        resultSet.add(entry)
        return render(request, "encyclopedia/sResults2.html", {"resultSet": resultSet, "allEnteries": allEnteries} )

def create(request):
    if request.method == "POST":
        print("inside create function")
        title = request.POST.get('t')
        content = request.POST.get('c')
        for entry in util.list_entries():
            if title == entry:
                return render(request,"encyclopedia/errorPage.html")
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse("wiki:index"))

    return render(request, "encyclopedia/create.html")

def edit(request, name):
    if request.method == "POST":
        title = name
        content = request.POST.get('c')
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse("wiki:page", kwargs={'name':name} ))
    return render(request, "encyclopedia/edit.html", {"entry": util.get_entry(name),"name": name })
    


