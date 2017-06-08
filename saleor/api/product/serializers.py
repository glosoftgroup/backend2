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
from ...product.models import (
    Product,
    ProductVariant,
    )

User = get_user_model()

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

class ProductListSerializer(serializers.ModelSerializer):    
    vat_tax = SerializerMethodField()
    item_price = SerializerMethodField()
    class Meta:
        model = Product
        fields = ('id', 'name', 'vat_tax','item_price')
    def get_vat_tax(self, obj):
        tax = obj.get_tax_value()
        return tax
    def get_item_price(self,obj):
        item_price = obj.price.gross
        return item_price

class ProductStockListSerializer(serializers.ModelSerializer):    
    #vat_tax = SerializerMethodField()
    #item_price = SerializerMethodField()
    class Meta:
        model = ProductVariant
        fields = ('id', 'display_product')


# PERMISSIONS SERIALIZERS
class PermissionListSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name='users-api:permission-detail')
    class Meta:
        model = Permission
        fields = ('id','url','codename')


