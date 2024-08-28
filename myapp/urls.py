
from django.urls import path,include
from .views import transaction_view,user_detail,upload_user_data_to_s3,index




urlpatterns = [
    path("",index.as_view()),
    path('users',user_detail.as_view()),
    path('users/<int:pk>',user_detail.as_view()),
    path('transaction',transaction_view.as_view()),
    path('upload-user-data/', upload_user_data_to_s3, name='upload_user_data'),
]
