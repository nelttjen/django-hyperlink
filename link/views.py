from django.shortcuts import render


# Create your views here.
def index(request, code):
    return render(request, 'links/index.html', {'code': code})

