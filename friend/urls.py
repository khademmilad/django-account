from django.urls import path
from friend.views import (
    send_friend_request,
)

app_name = 'friend'

urlpatterns = [
    # path("<int:id>/send/",send_friend_request,name="send_request"),
    path('friend_request/', send_friend_request, name='friend-request'),

]
