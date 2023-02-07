from django.shortcuts import render

from link.forms import ShareLinkForm, ShareLinkAuthorizedForm


# Create your views here.
def index(request, code):
    return render(request, 'links/index.html', {'code': code})


def create(request):
    form = ShareLinkForm() if not request.user.is_authenticated else ShareLinkAuthorizedForm()
    return render(request, 'links/create.html', context={'form': form})
