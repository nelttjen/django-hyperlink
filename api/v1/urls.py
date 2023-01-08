from django.urls import path
from users.api.register import RegisterView

link_patterns = [

]

users_patterns = [
	path('users/register/', RegisterView.as_view())
]

urlpatterns = [
	*link_patterns,
	*users_patterns,
]