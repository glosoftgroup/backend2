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
    Stock,
    )

User = get_user_model()

class CreateStockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        exclude = ['quantity_allocated']

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
        fields = (
            'id', 
            'name',
            'vat_tax',
            'item_price',
           )
    def get_vat_tax(self, obj):
        if obj.product_tax:
            tax = obj.product_tax.tax
        else:
            tax = 0
        return tax
    def get_item_price(self,obj):
        item_price = obj.price.gross
        return item_price


class ProductStockListSerializer(serializers.ModelSerializer):    
    productName = SerializerMethodField()
    price = SerializerMethodField()
    quantity = SerializerMethodField()
    productlist = UserListSerializer(required=False)
    tax =SerializerMethodField()
    class Meta:        
        model = ProductVariant
        fields = (
            'id',
            'productName',
            'sku',
            'price',
            'tax',
            'productlist',
            'quantity',
            )
    def get_quantity(self,obj):
        quantity = obj.get_stock_quantity()
        return quantity
    def get_productName(self,obj):
        productName = obj.display_product()
        return productName
    def get_price(self,obj):
        price = obj.get_price_per_item().gross
        return price
    def get_tax(self,obj):
        if obj.product.product_tax:
            tax = obj.product.product_tax.tax
        else:
            tax = 0        
        return tax



class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant         



# PERMISSIONS SERIALIZERS
class PermissionListSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name='users-api:permission-detail')
    class Meta:
        model = Permission
        fields = ('id','url','codename')


