from rest_framework import authentication
from rest_framework import exceptions
from users.models import User, UserToken
from django.utils.translation import ugettext_lazy as _

class IsUserAuthicated(authentication.BaseAuthentication):
	def authenticate(self, request):
		token = request.META.get('HTTP_ACCESS_TOKEN')
		if token is None:
			raise exceptions.AuthenticationFailed(_('UNAUTHORISED ACCESS! NO HEADER PROVIDED'))
		try:
			user_token = UserToken.objects.get(access_token=token)
		except User.DoesNotExist:
			raise exceptions.AuthenticationFailed('Unauthorised User')
			
		return (user_token.user.transform, user_token.transform)

class UserTokenAuthentication(authentication.BaseAuthentication):
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
		auth = UserToken.objects.create(**{'user_id':user['id']}).transform

		return (user, auth)
