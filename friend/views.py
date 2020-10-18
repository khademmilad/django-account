from django.shortcuts import render

# Create your views here.
def friend_requests(request, *args, **kwargs):

	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get("user_id")
	print()
	print(request.user.pk)

	return render(request, "friend/friend_requests.html", context)
