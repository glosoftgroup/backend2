from django.conf.urls import url

from .views import (
    UserListAPIView,
    UserDetailAPIView,
    UserCreateAPIView,
    UserDeleteAPIView,
    UpdateAPIView,
    PermissionListView,
    PermissionDetailAPIView
)


urlpatterns = [
    url(r'^$', UserListAPIView.as_view(), name='user-list'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^users-details/(?P<pk>[0-9]+)/$', UserDetailAPIView.as_view(), name='detail'),
    url(r'^edit/(?P<pk>[0-9]+)/$', UpdateAPIView.as_view(), name='edit'),
    url(r'^user-delete/(?P<pk>[0-9]+)/$', UserDeleteAPIView.as_view(), name='user-delete'),

    #permissions url patterns
    url(r'^permission-details/(?P<pk>[0-9]+)/$', PermissionDetailAPIView.as_view(), name='permission-detail'),
    url(r'^permissions', PermissionListView.as_view(), name='permissions')

]

