from .activate import ActivateView, ActivateSerializer
from .login import LoginView, LoginSerializer
from .register import RegisterView, RegisterSerializer
from .recovery import RecoveryView, RecoverySerializer
from .social import SocialAuthView, SocialUpdateView
from .test import TestView
from .profile import CurrentUserView, CurrentUserProfileSerializer, UserProfileSerializer, UserModeratorProfileSerializer

__all__ = (
    'ActivateView', 'ActivateSerializer',
    'LoginView', 'LoginSerializer',
    'RegisterView', 'RegisterSerializer',
    'RecoveryView', 'RecoverySerializer',
    'SocialAuthView', 'SocialUpdateView',

    'CurrentUserView', 'CurrentUserProfileSerializer', 'UserProfileSerializer', 'UserModeratorProfileSerializer',

    'TestView'
)