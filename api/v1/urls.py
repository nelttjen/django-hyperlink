from django.urls import path

from users.api import *
from link.api import *

link_patterns = [
	path('links/create/', LinkCreateView.as_view(), name='api-links-create'),

	path('links/<str:code>/', LinkView.as_view(), name='api-links-link')
]

users_patterns = [
	path('users/register/', RegisterView.as_view(), name='api-users-register'),
	path('users/activate/', ActivateView.as_view(), name='api-users-activate'),
	path('users/login/', LoginView.as_view(), name='api-users-login'),
	path('users/test/', TestView.as_view(), name='api-users-test'),
	path('users/recovery/', RecoveryView.as_view(), name='api-users-recovery'),
]

urlpatterns = [
	*link_patterns,
	*users_patterns,
]