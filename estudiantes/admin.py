from django import forms
from django.contrib import admin
from .models import Estudiante #Notas

class EstudianteAdminForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'

class EstudianteAdmin(admin.ModelAdmin):
    form = EstudianteAdminForm
    list_display = ('user', 'facultad', 'grupo')



admin.site.register(Estudiante, EstudianteAdmin)

