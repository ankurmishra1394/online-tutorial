from rest_framework import authentication
from rest_framework import exceptions
from users.models import User
from django.utils.translation import ugettext_lazy as _

class IsUserAuthicated(authentication.BaseAuthentication):
	def authenticate(self, request):
		username = request.META.get('X_USERNAME')
		if username is None:
			raise exceptions.AuthenticationFailed(_('UNAUTHORISED ACCESS! NO HEADER PROVIDED'))
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			raise exceptions.AuthenticationFailed('Unauthorised User')
		return (user, None)

class UserAuthentication(authentication.BaseAuthentication):
	def authenticate(self, request):
		username = request.data.get('username', None)
		password = request.data.get('password', None)

		if not username or not password:
			raise exceptions.AuthenticationFailed(_('No credentials provided.'))

		credentials = {
			'username':username,
			'password' : password
		}

		user = User.authenticate(credentials)
		return (user, None)
