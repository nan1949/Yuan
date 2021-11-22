from rest_framework import serializers
from .models import User
from rest_framework.authtoken.views import Token


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    # token生成放到Model中了
    # def create(self, validated_data):
    #     user = User.objects.create(**validated_data)
    #     Token.objects.create(user=user)
    #     return user

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'password', 'email', 'avatar']

        extra_kwargs = {'password': {
            'write_only': True,
            'style': {'input_type': 'password'},
            'required': True
        }}

