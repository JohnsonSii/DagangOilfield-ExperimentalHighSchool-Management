from django.urls import path

from . import views

urlpatterns = [
    path("testapi/", views.testApi),
    path("validateuserexist/", views.validateUserExist),
    path("register/", views.register),
    path("login/", views.login),
    path("receive/", views.receive),
    path("getuserinfo/", views.getUserInfo),
    path("getqrcode/", views.getQRCode),
    path("setuserpassed/", views.setUserPassed),
    path("getall/", views.getAll),
    path("getallnotpass/", views.getAllNotPass),
    path("getuserimage/", views.getUserImage),
]
