from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class ValidateUsername:

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя \'me\' запрещено!'
            )
        return username


class UserSerializer(serializers.ModelSerializer, ValidateUsername):
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all(),
                            message="Username должен быть уникальным"),
        ),
    )
    email = serializers.EmailField(
        validators=(
            UniqueValidator(queryset=User.objects.all(),
                            message="Emain должен быть уникальным"),
        ),
    )

    class Meta:
        model = User
        fields = ('username',
                  'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class RegisterUserSerializer(serializers.ModelSerializer, ValidateUsername):

    class Meta:
        model = User
        fields = ('username', 'email')


class AccessTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

