from django.contrib import admin
from .models import Grupo
from django.forms import ModelForm


# Register your models here.

class GrupoAdminForm(ModelForm):

    class Meta:
        model = Grupo
        fields = "__all__"
    
class GrupoAdmin(admin.ModelAdmin):

    form = GrupoAdminForm
    list_display = ['numero_grupo', 'facultad']



admin.site.register(Grupo, GrupoAdmin)