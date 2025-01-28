from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, ImageField
from rest_framework.serializers import ModelSerializer, Serializer

from user.models import User



class UserModelSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True, max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        password = validated_data.get('password')

        if password != confirm_password:
            raise ValidationError({'password': 'Passwords do not match'})

        user = User.objects.create_user(**validated_data)
        return user
class UserContinueModelSerializer(ModelSerializer):
    image=ImageField(required=False)
    class Meta:
        model=User
        fields=('secret_word','secret_number','passport_number','about','image')

class UserDeleteModelSerializer(ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
class UserLoginSerializer(Serializer):
    username=CharField(max_length=255)
    password=CharField(max_length=255)