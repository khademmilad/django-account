from django.urls import path
from account.views import login_view,home_view,registration_view

urlpatterns = [
    path("",home_view,name="home"),
    path('login/',login_view,name="login"),
    path("register/",registration_view,name="register"),

]
