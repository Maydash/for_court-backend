from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from .filters import *
from .views import *

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    path('api/getlogos', LogoAPI.as_view(), name='logo-api'),
    path('api/allcategories', CategoryList.as_view(), name='all-categories'),
    path('api/login', LoginAPI.as_view(), name='login-api'),
    path('api/recipientconfigbyid/<int:id>', recipient_detail, name='configure-recipients-by-id'),  #algydar
    path('api/getrecipientchildren/<int:id>', get_recipient_children, name='recipient-children'),   #algydaryn chagalary
    path('api/getrecipientchildbyid_updateordelete/<int:recipient_id>/<int:child_id>', get_recipient_child_by_id_update_delete, name='child-by-id'),
    path('api/getallmustpays', MustPayList.as_view(), name='all-mustpays'),   #####
    path('api/mustpayconfigbyid/<int:id>', mustpay_detail, name='configure-must-pays-by-id'),   ######    bergidar
    path('api/mustpayreceipts/<int:id>', get_mustpay_receipts, name='all-mustpay-receipts'),    #bgidaryn tolegi
    path('api/mustpayreceiptsbyid_deleteorpatch/<int:mustpay_id>/<int:receipt_id>', get_receipt__by_id_update_delete, name='configure-receipt-by-id'),
    path('api/getinsolvents', InsolventsSinceThreeMonths, name='insolvent-api'),  #####
    path('api/getallalimonies', AlimonyList.as_view(), name='all-alimonies'),
    path('api/alimonyconfigbyid/<int:id>', AlimonyDetail.as_view(), name='alimony-configure-by-id'),
    path('api/archivealimonies', ArchiveList.as_view(), name='all-archive-alimonies'),
    re_path(r'^api/allalimonies/filter/$', FilteringAlimony.as_view(), name='filtering-all-alimonies'),
    re_path(r'^api/allrecipients/filter/$', FilteringRecipient.as_view(), name='filtering-all-recipients'),
    re_path(r'^api/allmustpays/filter/$', FilteringMustPay.as_view(), name='filtering-all-mustpays'),
    path('api/addalimony', add_alimony, name='adding-alimony'),

    path('api/mustpayreceipts/undefined', pass_undefined),
    path('api/mustpayconfigbyid/undefined', pass_undefined),
    path('api/getrecipientchildren/undefined', pass_undefined),
    path('api/recipientconfigbyid/undefined', pass_undefined)
]
