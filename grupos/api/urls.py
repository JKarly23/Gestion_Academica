from django.urls import path
from .views import GruposListAV,GrupoDetailAV

urlpatterns = [
    path("", GruposListAV.as_view(), name="grupos-list"),
    path("<int:pk>/", GrupoDetailAV.as_view(), name="grupo-detail"),
]

