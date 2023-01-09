from django.shortcuts import render


def login(request):
    message = request.GET.get('message', '')
    return render(request, 'users/login.html', {'message': message})


def activate(request):
    code = request.GET.get('code', '')
    return render(request, 'users/activate.html', {'code': code})