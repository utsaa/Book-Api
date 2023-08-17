"""Book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="handleSignup"),
    path('login/', views.gologin, name="login"),
    path('logout/', views.handlelogout, name="logout"),
    path('isbn/', views.isbn, name="isbn"),
    path('search/', views.search, name="search"),
    path('isbnshow/', views.isbnshow, name="isbnshow"),
    path('isbnname', views.isbnname, name="isbnname"),
    path('handlelogin', views.handlelogin, name="handleLogin"),
    path('handleisbn', views.handleisbn, name="handleisbn"),
    path('isbnsave', views.isbnsave, name="isbnsave"),
    path('isbndelete', views.isbndelete, name="isbndelete"),
    path('show', views.show, name="show"),
]
