from django.urls import path
from .views import facultad_list,facultad_detail

urlpatterns = [
    path("",facultad_list, name="facultad-list"),
    path("<int:pk>/",facultad_detail, name="facultad-detail"),
]
