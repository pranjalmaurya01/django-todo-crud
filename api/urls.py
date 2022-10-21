"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# from rest_framework import routers
from django.shortcuts import redirect
from django.urls import path
from . import views


# router = routers.SimpleRouter()
# router.register('signup/', views.SignUpView, basename="signup")

urlpatterns = [
    path('', lambda request: redirect('home', permanent=True)),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.Login.as_view(), name="login"),
    path("home/", views.Home.as_view(), name="home"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("add_todo/", views.AddTodo.as_view(), name="add_todo"),
    path("change_status/<int:pk>/<str:status>",
         views.ChangeTodoStatus.as_view(), name="change_status"),
    path("delete_todo/<int:pk>", views.DeleteTodo.as_view(), name="delete_todo"),
]
