from django.urls import path,include
from .views import ProfesorListAV,ProfesorDetailAV


urlpatterns = [
    path("",ProfesorListAV.as_view(), name="profesor-list"),
    path("<int:pk>/", ProfesorDetailAV.as_view(), name="Profesor-detail"),
]
