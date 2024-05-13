from django.contrib import admin
from .models import Facultad
from django.forms import ModelForm

# Register your models here.
class FacultadAdminForm(ModelForm):
    class Meta:
        model = Facultad
        fields = "__all__"


class FacultadAdmin(admin.ModelAdmin):

    form = FacultadAdminForm
    list_display = ['name']

admin.site.register(Facultad, FacultadAdmin)