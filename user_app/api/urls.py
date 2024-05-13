from django.urls import path
from .views import registrar,loggin,cerrar_sesion,AccountListAv,AccountDetail,myprofile
from rest_framework_simplejwt.views import TokenBlacklistView


urlpatterns = [
    path('register/',registrar,name='user-register'),
    path("loggin/", loggin, name="loggin-user"),
    path('logout/', cerrar_sesion, name='token_blacklist'),
    path("", AccountListAv.as_view(), name="account-list"),
    path("<int:pk>", AccountDetail.as_view(), name="account-detail"),
    path("myprofile/",myprofile,name="myprofile"),
]
