from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from .views import *

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    path('api/getlogos', logo_api, name='logo-api'),
    path('api/login', login_api, name='login-api'),
    path('api/getrecipientbyid/<int:id>', get_recipient_by_id, name='recipient-by-id'),
    path('api/addrecipient', add_recipient, name='adding-recipient'),
    path('api/getrecipientchildren/<int:id>', get_recipient_children, name='recipient-children'),
    path('api/getrecipientchildbyid/<int:recipient_id>/<int:child_id>', get_recipient_child_by_id, name='child-by-id'),
    path('api/addrecipientchild', add_recipient_child, name='adding-recipient-child'),
]
