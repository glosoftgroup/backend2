from rest_framework.serializers import (
    EmailField,
    CharField,
    BooleanField,
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError
    )
from django.contrib.auth.models import Permission
from rest_framework import serializers
from django.contrib.auth import get_user_model
#from userModule.models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    ''' 
        profile serilizers.
    '''

    class Meta:
        model = User
        fields = ['email',]


class UserCreateSerializer(ModelSerializer):
    email    = EmailField(label='Email address')
    #profile  = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = [            
            'email',
            'password',  
            'is_staff',            
        ]
        extra_kwargs = {'password':
                            {'write_only':True}
                        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }


class UserListSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name='users-api:detail')
    delete_url = HyperlinkedIdentityField(view_name='users-api:user-delete')
    #profile = ProfileSerializer(required=False, )

    class Meta:
        model = User
        fields = ('id', 'email', 'url', 'delete_url')





# PERMISSIONS SERIALIZERS
class PermissionListSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name='users-api:permission-detail')
    class Meta:
        model = Permission
        fields = ('id','url','codename')


