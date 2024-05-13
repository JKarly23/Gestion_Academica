from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AsignaturasVS,ComentarioListAV,NotasListAV,NotasDetailAV,CometarioDetailAV

router = DefaultRouter()
router.register("asignaturas", AsignaturasVS, basename="asignaturas")


urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/comentarios/", ComentarioListAV.as_view(), name="comentario-list"),
    path("comentarios/<int:pk>/", CometarioDetailAV.as_view(),name="comentario-detail"),
    path("estudiante/<int:pk>/notas/", NotasListAV.as_view(),name="notas-list"),
    path("nota/<int:pk>",NotasDetailAV.as_view(),name="notas-detail"),
]
