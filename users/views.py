# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import mixins, viewsets
from users.models import User
from rest_framework.views import APIView
from serializers import UserSerializer
from users.authentication import IsUserAuthicated, UserAuthentication
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

class AuthViewSet(APIView):
	queryset = User.objects.all()
	authentication_classes = (UserAuthentication, )

	def post(self, request, format=None):
		content = {
			'user': request.user,
			'auth': request.auth,
		}
		return Response(content)