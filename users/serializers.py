from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
	id = serializers.ReadOnlyField()
	password = serializers.CharField(write_only=True, style={'input_type':'password'})

	class Meta:
		model = User
		fields = ('id', 'first_name', 'middle_name', 'last_name', 'username', 'email', 'password')

	def create(self, validated_data):
		user = super(UserSerializer, self).create(validated_data)
		user.set_password(validated_data['password'])
		user.set_reset_code()
		user.save()
		return user

	def update(self, instance, validated_data):
		instance.first_name = validated_data.get('first_name', instance.first_name)
		instance.middle_name = validated_data.get('middle_name', instance.middle_name)
		instance.last_name = validated_data.get('last_name', instance.last_name)
		if 'password' in validated_data:
			instance.set_password(validated_data['password'])
		instance.save()
		return instance