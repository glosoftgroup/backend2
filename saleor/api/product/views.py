from django.db.models import Q

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    )

from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     UpdateAPIView,
                                     RetrieveUpdateAPIView)
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.models import Permission
from ...product.models import (
    Product,
    ProductVariant,
    Stock,
    )
from .serializers import (
    CreateStockSerializer,
    ProductStockListSerializer,
    ProductListSerializer,
    UserListSerializer,    
    UserCreateSerializer,
    PermissionListSerializer,   
     )
from rest_framework import generics


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()

class CreateStockAPIView(CreateAPIView):
    serializer_class = CreateStockSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Stock.objects.all()


# class UserCreateAPIView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserCreateSerializer
#
#     def perform_create(self, serializer):
#         #user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#         serializer.save(user=self.request.user)


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class ProductListAPIView(generics.ListAPIView):
    #permission_classes = [IsAuthenticatedOrReadOnly]    
    pagination_class = PostLimitOffsetPagination
    serializer_class = ProductListSerializer

    def get_queryset(self, *args, **kwargs):        
        queryset_list = Product.objects.all().select_related()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(name__icontains=query)|
                Q(variants__sku__icontains=query)|
                Q(categories__name__icontains=query)
                ).distinct()
        return queryset_list

class ProductStockListAPIView(generics.ListAPIView):
    #permission_classes = [IsAuthenticatedOrReadOnly]    
    pagination_class = PostLimitOffsetPagination
    serializer_class = ProductStockListSerializer

    def get_queryset(self, *args, **kwargs):        
        queryset_list = ProductVariant.objects.all().select_related()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(sku__icontains=query) |
                Q(product__name__icontains=query)
                ).distinct()
        return queryset_list

class UserListAPIView(generics.ListAPIView):
    #permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserListSerializer


# Permissions views
class PermissionListView(generics.ListAPIView):
    serializer_class = PermissionListSerializer
    queryset = Permission.objects.all()


class PermissionDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PermissionListSerializer
    queryset = Permission.objects.all()








