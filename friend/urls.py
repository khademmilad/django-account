from django.urls import path
from friend.views import ( friend_requests,
)

app_name = 'friend'

urlpatterns = [
    path("",friend_requests,name="home"),

]
