from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import json
from urllib.request import urlopen

from .models import BookInfo
from .templatetags import extras
import json
# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def signup(request):
    if request.method=="POST":
        username= request.POST.get("username")
        email= request.POST.get("email")
        fname= request.POST.get("fname")
        lname= request.POST.get("lname")
        pass1= request.POST.get("pass1")
        pass2= request.POST.get("pass2")

        if pass1!=pass2:
            messages.error(request, "Passwords does not match")
            return redirect("home")
        try:
            myuser=User.objects.create_user(username, email,pass1)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()
        except:
            messages.error(request, "You are already signed in")
        
        return redirect("isbn")
    else:
        HttpResponse("404 - Not Found")

def handlelogin(request):
    if request.method=="POST":
        loginusername=request.POST["loginusername"]
        loginpassword=request.POST["loginpassword"]
        user=authenticate(username=loginusername, password=loginpassword)
        
        if user is not None:
            login(request,user)
            messages.success(request,"You have been sucessfully logged in ")
            return redirect("isbn")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("home")
    return HttpResponse("404 - Not found")

def gologin(request):
    if request.user.is_authenticated:  return redirect("home")
    return render(request, "home/login.html")

def handlelogout(request):
    logout(request)
    messages.success(request, " You have been sucessfully logged out")
    return redirect("home")
    
def isbn(request):
    return render(request, "home/isbn.html")

def handleisbn(request):
    api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

    IsbnNum=request.GET['isbninp']

    res=urlopen(api+IsbnNum)
    json_data=json.load(res)
    try:
        volume_info=json_data['items']
    except:
        messages.error(request, "Invalid ISBN")
        return redirect("isbn")
    n=len(volume_info)
    if not n:
        messages.error(request, "Invalid ISBN")
        return redirect("isbn")
    n=n if n<25 else 25
    context={"VolInfo": volume_info[:n]}
    return render(request, 'home/IsbnShow.html', context)

def isbnsave(request):
    if request.method=='POST':
        
        title=request.POST['IsbnTitle']
        authors=request.POST['IsbnAuthors']
        page_count=request.POST['IsbnPage']
        average_rating=request.POST["IsbnRating"]
        user=request.user
        if page_count=="None": page_count=0
        if average_rating=="None": average_rating=0
        
        pres= BookInfo.objects.filter(user=user, title=title, authors=authors)
        if pres: 
            
            messages.warning(request, "Your Book is already Stored")
            res={"msg": "False"}
            res=json.dumps(res)
            return HttpResponse(res , content_type="application/json")
        bk=BookInfo( user=user, title=title,authors=authors, pageCount=page_count, averageRating=average_rating )
        messages.success(request,"you Book is saved")
        bk.save()
        res={"msg": "True"}
        res=json.dumps(res)
        return HttpResponse(res , content_type="application/json")
        # return render(request, 'home/IsbnShow.html')
    return HttpResponse("404 - Not Found")

def show(request):
    bk=BookInfo.objects.filter(user=request.user)
    title=[i.title for i in bk]
    authors=[i.authors for i in bk]
    page_count=[i.pageCount for i in bk]
    average_count=[i.averageRating for i in bk]
    ins=[i.id for i in bk]
    # print("ins list is",ins)
    book=list(zip(title,authors, page_count,average_count,ins))
    context={"book": book}
    return render(request, 'home/show.html', context)

def isbndelete(request):
    if request.method=='POST':
        insid=request.POST['IsbnDelete']
        # print("before", insid)
        # nb=len('BookInfo')
        insdel=BookInfo.objects.get(id=int(insid))
        # print("after",insid)
        insdel.delete()
        messages.success(request, "The book has been success fully deleted")
        res={"msg": "True"}
        res=json.dumps(res)
        return HttpResponse(res, content_type='application/json')
    return HttpResponse('404 - Not Found')

def isbnshow(request):
    return render(request, 'home/IsbnShow.html')

def isbnname(request):
    # if request.method=="POST":

    api = "https://www.googleapis.com/books/v1/volumes?q=intitle:"

    title=request.GET["isbninpname"]
    title=title.replace(" ","+")
    
    res=urlopen(api+title)
    json_data=json.load(res)

    try:
        volume_info=json_data['items']
    except:
        messages.error(request, "Invalid title")
        return redirect("isbn")
    n=len(volume_info)
    if not n:
        messages.error(request, "Invalid Title")
        return redirect("isbn")
    n=n if n<25 else 25
    context={"VolInfo": volume_info[:n]}
    return render(request, 'home/IsbnShow.html', context)


def search(request):
    query=request.GET["query"]
    if len(query)>250:
        info=BookInfo.objects.none()
    else:
        info1=BookInfo.objects.filter(title__icontains=query)
        info2=BookInfo.objects.filter(authors__icontains=query)
    if not info1 and not info2:
        messages.warning(request, "No search result found")
        return redirect("home")
    info=info1.union(info2)
    title=[i.title for i in info]
    authors=[i.authors for i in info]
    page_count=[i.pageCount for i in info]
    average_count=[i.averageRating for i in info]
    ins=[i.id for i in info]
    # print("ins list is",ins)
    book=list(zip(title,authors, page_count,average_count,ins))
    context={"book": book}
    return render(request, 'home/show.html', context)
