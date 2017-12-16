# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import EmailValidator
from django.utils import timezone

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
							})
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

class Users(AbstractBaseUser):
	reset_code = models.CharField(_('reset code'), max_length=255)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'user'

	def __str__(self):
		return self.username
		