from django.contrib.auth.models import User
from django.utils import timezone

from users.models import ActivateCode
from users.tasks.user_code import send_activation_code


class Email:
	def __init__(self, user_id):
		self.user = User.objects.filter(id=user_id).first()

	def send_activation_mail(self):
		if not self.user:
			return False
		email = self.user.email
		if not (code := ActivateCode.objects.filter(user=self.user, is_used=False,
		                                            expired_date__gte=timezone.now()).first()):
			code = ActivateCode(user=self.user, type=1).generate_code()
		send_activation_code.delay(code.code, email)
		return True