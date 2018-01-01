from rest_framework import authentication
from rest_framework import exceptions
from users.models import User, UserToken
from django.utils.translation import ugettext_lazy as _
from rest_framework.parsers import JSONParser

class IsUserAuthicated(authentication.BaseAuthentication):
	def authenticate(self, request):
		token = request.META.get('HTTP_ACCESS_TOKEN')
		if token is None:
			raise exceptions.AuthenticationFailed(_('UNAUTHORISED ACCESS! NO HEADER PROVIDED'))
		try:
			user_token = UserToken.objects.get(access_token=token)
		except Exception:
			raise exceptions.AuthenticationFailed(_('Invalid token provided'))

		if not user_token.user.is_active:
			raise exceptions.AuthenticationFailed(_('Account not activated or deleted!'))

		return (user_token.user.transform, user_token.transform)

class UserTokenAuthentication(authentication.BaseAuthentication):
	def authenticate(self, request):
		data = JSONParser().parse(request)
		username = data['username']
		password = data['password']

		if not username or not password:
			return ('Anonymous User', None)
			# raise exceptions.AuthenticationFailed(_('No credentials provided.'))

		credentials = {
			'username':username,
			'password' : password
		}

		user = User.authenticate(credentials)
		auth = UserToken.objects.create(**{'user_id':user['id']}).transform

		return (user, auth)
		