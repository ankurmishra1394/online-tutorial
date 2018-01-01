# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import mixins, viewsets, status
from users.models import User
from rest_framework.views import APIView
from serializers import UserSerializer
from users.authentication import IsUserAuthicated, UserTokenAuthentication
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def user_signin(request):
	try:
		authenticate = UserTokenAuthentication().authenticate(request)
		request.user = authenticate[0]
		request.auth = authenticate[1]
		content = {
			'user' : request.user,
			'auth' : request.auth,
		}
	except Exception as e:
		return JsonResponse(str(e), status=e.status_code, safe=False)
	return JsonResponse(content, status=status.HTTP_200_OK)

@csrf_exempt
def user_signup(request):
	data = JSONParser().parse(request)
	serializer = UserSerializer(data=data)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, status=201)
	return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def account_activate(request):
	try:
		user = User.objects.get(**{'reset_code':request.GET.get('code', None)})
		user.is_active = True
		user.reset_code = ''
		user.save()
		return JsonResponse({'message':'Account Activated Successfully. Please Login!'}, status=status.HTTP_200_OK)
	except Exception:
		return JsonResponse({'message':'Invalid Code Provided'}, status=status.HTTP_400_BAD_REQUEST)

class UserMixin(object):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	authentication_classes = (IsUserAuthicated, )

class UserViewSet(UserMixin, 
				# mixins.CreateModelMixin,
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
		return Response(content, status=status.HTTP_200_OK)
