from django.shortcuts import render,redirect,get_object_or_404
from .forms import AccountAuthenticationForm,RegistrationForm
from django.contrib.auth import login, authenticate, logout

def home_view(request):

	return render(request,"home.html",{})




def registration_view(request):
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get("password1")
			account = authenticate(email=email,password=raw_password)
			login(request,account)
			return redirect('home')
	else:
		form = RegistrationForm()
		context = {
			"register_form" : form
		}
	return render(request,'account/register.html',context)






def login_view(request, *args, **kwargs):

	user = request.user
	if user.is_authenticated:
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get("email")
			raw_password = form.cleaned_data.get("password")
			user = authenticate(email=email, password=raw_password)

			if user:
				login(request,user)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context = {
		"login_form" : form
	}

	return render(request,"account/login.html",context)
