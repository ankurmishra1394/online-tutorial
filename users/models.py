# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
from rest_framework import exceptions
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import EmailValidator
from django.utils import timezone
from django.contrib.auth.hashers import (
	check_password, is_password_usable, make_password,
)
from datetime import datetime, timedelta

class AbstractUUIDBaseClass(models.Model):
	id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)

	REQUIRED_FIELDS = ['id']

	class Meta:
		abstract=True

class AbstractBaseUser(AbstractUUIDBaseClass):
	username_validator = ASCIIUsernameValidator()
	email_validator = EmailValidator()
	username = models.CharField(
					_('username'),
					max_length=150,
					unique=True,
					help_text=_('Required. 150 words or fewer. Letter, digits, and @/./+/-/_ only'),
					validators=[username_validator],
					error_messages={
						'unique':_("A user with that username already exists")
					},
				)
	password = models.CharField(_('password'), max_length=128)
	first_name = models.CharField(_('first name'), max_length=50, blank=False)
	middle_name = models.CharField(_('middle name'), max_length=50, blank=True)
	last_name = models.CharField(_('last name'), max_length=50, blank=True)
	email = models.CharField(
					_('email address'), 
					blank=False, 
					max_length=255,
					unique=True,
					validators=[email_validator],
					error_messages={
						'unique':_("Provided email-id already exists.")
					},
				)
	is_active = models.BooleanField(_('active'), default=False)

	REQUIRED_FIELDS=['username', 'email', 'first_name']


	class Meta:
		abstract=True
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def get_full_name(self):
		'''
		Return first_name plus middle_name plus last_name with space in between
		'''
		full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		'''
		Return only first_name
		'''
		return self.first_name.strip()

	def set_password(self, raw_password):
		self.password = make_password(raw_password)

	def set_reset_code(self):
		self.reset_code = str(uuid.uuid4())

class User(AbstractBaseUser):
	reset_code = models.CharField(_('reset code'), max_length=255)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'user'

	def __str__(self):
		return self.username

	@property
	def transform(self):
		return {
			'id' : self.id,
			'username' : self.username,
			'email' : self.email,
			'displayName' : self.get_full_name(),
			'joinedOn' : self.date_joined,
			'updatedOn' : self.updated_at
		}

	@staticmethod
	def authenticate(credentials):
		user = User.objects.filter(**{'username':credentials['username']})
		if not len(user):
			raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

		if not user[0].is_active:
			raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

		return user[0].transform

class UserToken(AbstractUUIDBaseClass):
	access_token = models.CharField(max_length=255, default=uuid.uuid4)
	user = models.ForeignKey('User', on_delete=models.CASCADE)
	expires_at = models.DateTimeField(_('expire datetime'), default=datetime.now()+timedelta(days=2))
	created_at = models.DateTimeField(_('created datetime'), default=timezone.now)

	class Meta:
		db_table = 'user_token'

	def __str__(self):
		return self.user.username

	@property
	def transform(self):
		return {
			'id' : self.id,
			'token' : self.access_token,
			'user' : self.user.transform,
			'createdAt' : self.created_at
		}
