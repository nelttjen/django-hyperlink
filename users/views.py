from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone


def test(request):
	print(timezone.now().timestamp())
	return render(request, 'users/test.html')


def login(request):
	message = request.GET.get('message', '')
	return render(request, 'users/login.html', {'message': message})


def register(request):
	return render(request, 'users/register.html')


def activate(request):
	code = request.GET.get('code', '')
	info = request.GET.get('info', '')
	return render(request, 'users/activate.html', {'code': code, 'info': info})


def recovery(request):
	code = request.GET.get('code', '')
	return render(request, 'users/recovery.html', {'code': code})
