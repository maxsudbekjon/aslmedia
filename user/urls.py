from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenVerifyView
from user.views import UserCreateAPIView, user_register_continue, UserDeleteAPIView, user_login

urlpatterns=[
    path('register',UserCreateAPIView.as_view()),
    path('register/delete/<int:id>',UserDeleteAPIView.as_view()),
    path('register/continue/<int:id>',user_register_continue),
    path('login/',user_login),
path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)