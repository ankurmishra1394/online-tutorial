from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
	id = serializers.ReadOnlyField()
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ('id', 'first_name', 'middle_name', 'last_name', 'username', 'email', 'password')

	def create(self, validated_data):
		user = super(UserSerializer, self).create(validated_data)
		user.set_password(validated_data['password'])
		user.set_reset_code()
		user.save()
		return user