from django import forms


class ShareLinkForm(forms.Form):
    redirect_to = forms.URLField()
    valid_until = forms.ChoiceField(choices=('1 переход', '1 день', '1 неделя', '1 месяц'))


class ShareLinkAuthorizedForm(ShareLinkForm):
    valid_until = forms.ChoiceField(choices=('1 день', '1 неделя', '1 месяц'))
    redirect_timer = forms.ChoiceField(choices=("Без таймера", "1 секунда", '3 секунды', '5 секунд', '10 секунд'))
    allowed_redirects = 