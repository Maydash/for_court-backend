from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from .views import *

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    path('api/logos', logo_api, name='logo-api'),
    path('api/login', login_api, name='login-api')
]
