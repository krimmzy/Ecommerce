# from django.contrib.auth.backends import BaseBackend
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class CustomBackend(BaseBackend):
# 	def authenticate(self, request, email=None, password=None):
# 		try:
# 			user = User.objects.get(email=email)
# 			if user.check_password(password):
# 				return user
# 			else:
# 				return None
# 		except ObjectDoesNotExist:
# 			return None