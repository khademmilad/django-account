from django.urls import path
from group.views import (
    group_index,
    create_group_form
)

app_name = 'group'

urlpatterns = [
    path('index',group_index,name='groups'),
    path('create_group',create_group_form,name="create_group")
]
