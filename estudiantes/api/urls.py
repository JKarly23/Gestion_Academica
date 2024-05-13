from django.urls import path
from .views import EstudiantesDetailAV,EstudiantesListAV

urlpatterns = [
    path("",EstudiantesListAV.as_view(), name="estudiantes-list"),
    path("<int:pk>/",EstudiantesDetailAV.as_view(), name="estudiante-detail"),
]
