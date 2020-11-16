from django.shortcuts import render
from .forms import CreateGroupForm


def group_index(request):
    return render(request,'group/index.html')


def create_group_form(request):
    form = CreateGroupForm(request.POST)
    if request.POST and form.is_valid():
        form.save()
    form = CreateGroupForm()
    dic = {
        'form' : form
    }
    return render(request,"group/create_group.html",dic)
