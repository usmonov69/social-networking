from django.shortcuts import render

def home(request):
	user = request.user
	hello = "Welcome"

	context  = {
	'user': user,
	'hello': hello,
	}
	return render(request, 'main/home.html', context)
