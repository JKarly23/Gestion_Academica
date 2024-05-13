from django.urls import path, include
from .views import AsignaturasDetailAV,AsignaturasVS,ComentarioListAV,NotasListAV,NotasDetailAV,CometarioDetailAV



urlpatterns = [
    path("", AsignaturasVS.as_view(), name="asignaturas-list"),
    path("<int:pk>/", AsignaturasDetailAV.as_view(), name="asignatura-detail"),
    path("<int:pk>/comentarios/", ComentarioListAV.as_view(), name="comentario-list"),
    path("comentarios/<int:pk>/", CometarioDetailAV.as_view(),name="comentario-detail"),
    path("estudiante/<int:pk>/notas/", NotasListAV.as_view(),name="notas-list"),
    path("nota/<int:pk>",NotasDetailAV.as_view(),name="notas-detail"),
]
