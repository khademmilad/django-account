from django.shortcuts import render,redirect,get_object_or_404
from .forms import AccountAuthenticationForm,RegistrationForm,AccountUpdateForm
from django.contrib.auth import login, authenticate, logout
from .models import Account
from django.http import HttpResponse
from django.conf import settings
from django.core import files
from friend.models import FriendList
from friend.utils import get_friend_request_or_false
from friend.friend_request_status import FriendRequestStatus




def home_view(request):
	queryset = Account.objects.all()
	dic = {
		"queryset" : queryset
	}
	return render(request,"home.html",dic)





def profile_view(request, *args, **kwargs):
	"""
	- Logic here is kind of tricky
		is_self
		is_friend
			-1: NO_REQUEST_SENT
			0: THEM_SENT_TO_YOU
			1: YOU_SENT_TO_THEM
	"""
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return HttpResponse("Something went wrong.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['profile_image'] = account.profile_image.url
		context['hide_email'] = account.hide_email

		friend_list = FriendList.objects.get(user=account)
		friends = friend_list.friends.all()
		context['friends'] = friends

		# Define template variables
		is_self = True
		is_friend = False
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # range: ENUM -> friend/friend_request_status.FriendRequestStatus
		friend_requests = None
		user = request.user
		if user.is_authenticated and user != account:
			is_self = False
			if friends.filter(pk=user.id):
				is_friend = True
			else:
				is_friend = False
				# CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
				if get_friend_request_or_false(sender=account, receiver=user) != False:
					request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
					context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
				# CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
				elif get_friend_request_or_false(sender=user, receiver=account) != False:
					request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				# CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
				else:
					request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

		elif not user.is_authenticated:
			is_self = False
		else:
			try:
				friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
			except:
				pass

		# Set the template variables to the values
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['request_sent'] = request_sent
		context['friend_requests'] = friend_requests
		context['BASE_URL'] = settings.BASE_URL
		return render(request, "account/profile.html", context)






def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated:
		return HttpResponse("You are already authenticate as " + str(user.email))

	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			destination = kwargs.get("next")
			if destination:
				return redirect(destination)
			return redirect('account:home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)






def login_view(request, *args, **kwargs):

	user = request.user
	if user.is_authenticated:
		return redirect("account:home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get("email")
			raw_password = form.cleaned_data.get("password")
			user = authenticate(email=email, password=raw_password)

			if user:
				login(request,user)
				return redirect("account:home")

	else:
		form = AccountAuthenticationForm()

	context = {
		"login_form" : form
	}

	return render(request,"account/login.html",context)


def logout_view(request):
	print("LOGGING OUT")
	logout(request)
	return redirect("account:home")




def edit_account_view(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("account:login")
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	if account.pk != request.user.pk:
		return HttpResponse("You cannot edit someone elses profile.")
	context = {}
	if request.POST:
			form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
			if form.is_valid():
				form.save()
				new_username = form.cleaned_data['username']
				return redirect("account:home")
			else:
				form = AccountUpdateForm(request.POST, instance=request.user,
					initial={
						"id": account.pk,
						"email": account.email,
						"username": account.username,
						"profile_image": account.profile_image,
						"hide_email": account.hide_email,
					}
				)
				context['form'] = form
	else:
		form = AccountUpdateForm(
			initial={
					"id": account.pk,
					"email": account.email,
					"username": account.username,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
				}
			)
		context['form'] = form
	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
	return render(request, "account/edit_account.html", context)
