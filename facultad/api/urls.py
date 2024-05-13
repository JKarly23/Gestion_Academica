from django.urls import path
from .views import FacultadListAV,FacultadDetailAV

urlpatterns = [
    path("",FacultadListAV.as_view(), name="facultad-list"),
    path("<int:pk>/",FacultadDetailAV.as_view(), name="facultad-detail"),
]
