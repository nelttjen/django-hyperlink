from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect as redirect
from django.contrib.auth import logout as logout_user
from django.urls import reverse
from django.utils import timezone
from oauth2_provider.models import AccessToken


def test(request):
    print(timezone.now().timestamp())
    return render(request, 'users/test.html')


def login(request):
    
    if request.user.is_authenticated:
        return redirect('/users/profile/')
    
    message = request.GET.get('message', '')
    next_link = ''
    if redirect_location := request.GET.get('next'):
        next_link = f'&next={redirect_location}'
    vk_link = reverse('socials') + '?provider=vk' + next_link

    return render(request, 'users/login.html', {'message': message, 'vk_link': vk_link})


def register(request):
    return render(request, 'users/register.html')


def activate(request):
    code = request.GET.get('code', '')
    info = request.GET.get('info', '')
    return render(request, 'users/activate.html', {'code': code, 'info': info})


def recovery(request):
    code = request.GET.get('code', '')
    return render(request, 'users/recovery.html', {'code': code})


def logout(request):
    if token := request.COOKIES.get('token'):
        if token := AccessToken.objects.filter(token=token).first():
            token.delete()
            logout_user(request)
    response = redirect(reverse('users-login') + '?message=Вы вышли с аккаунта')
    response.delete_cookie('token')
    response.delete_cookie('user_id')
    return response


def socials(request):
    if request.GET.get('provider') == 'tg':
        return render(request, 'users/telegram.html')
    return render(request, 'users/socials.html')


def socials_vk(request):
    return render(request, 'users/socials_vk_proceed.html')


@login_required
def profile(request):
    return render(request, 'users/profile.html')