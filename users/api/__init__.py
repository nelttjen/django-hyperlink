from .activate import ActivateView, ActivateSerializer
from .login import LoginView, LoginSerializer
from .register import RegisterView, RegisterSerializer
from .recovery import RecoveryView, RecoverySerializer
from .social import SocialAuthView
from .test import TestView

__all__ = (
    'ActivateView', 'ActivateSerializer',
    'LoginView', 'LoginSerializer',
    'RegisterView', 'RegisterSerializer',
    'RecoveryView', 'RecoverySerializer',
    'SocialAuthView',

    'TestView'
)