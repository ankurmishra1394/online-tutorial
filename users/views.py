# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import mixins, viewsets, status
from users.models import User
from rest_framework.views import APIView
from serializers import UserSerializer
from users.authentication import IsUserAuthicated, UserTokenAuthentication
from rest_framework.response import Response

class UserMixin(object):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	authentication_classes = (IsUserAuthicated, )

class UserViewSet(UserMixin, 
				mixins.CreateModelMixin,
				mixins.ListModelMixin,
				mixins.RetrieveModelMixin,
				mixins.UpdateModelMixin,
				mixins.DestroyModelMixin,
				viewsets.GenericViewSet):
	pass

class AuthViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	queryset = User.objects.all()
	authentication_classes = (UserTokenAuthentication, )
	serializer_class = UserSerializer
	lookup_field = 'reset_code'

	def retrieve(self, request, reset_code):
		try:
			user = User.objects.get(**{'reset_code':reset_code})
			user.is_active = True
			user.reset_code = ''
			user.save()
			return Response({'message':'Account Activated Successfully. Please Login!'}, status=status.HTTP_200_OK)
		except Exception:
			return Response({'message':'Invalid Code Provided'}, status=status.HTTP_400_BAD_REQUEST)

	def create(self, request, format=None):
		content = {
			'user': request.user,
			'auth': request.auth,
		}
		return Response(content)
