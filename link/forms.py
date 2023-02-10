from django import forms

from link.models import ShareLink


class ShareLinkForm(forms.Form):
    choices = (
        (1, '1 день'),
        (7, '1 неделя'),
        (30, '1 месяц'),
        (-1, 'Никогда'),
    )

    redirect_to = forms.URLField(label='Ссылка', widget=forms.URLInput(attrs={'class': 'form-control'}))
    valid_until = forms.ChoiceField(label='Действительна', choices=choices, initial=7)


class ShareLinkAuthorizedForm(ShareLinkForm):

    redirect_timer = forms.ChoiceField(label='Время перед переадрисацией', choices=ShareLink.redirect_time_choices, initial=5)
    allowed_redirects = forms.IntegerField(label='Максимальное кол-во редиректов (-1 - нет ограничений)', initial=-1)
    only_unique_redirects = forms.BooleanField(label='Считать только уникальные переходы?')
    is_active = forms.BooleanField(label='Доступна?', initial=True)

