from django.contrib import admin
from django import forms
from .models import Profesor
# Register your models here.


class ProfesorFormsAdmin(forms.ModelForm):

    class Meta:
        model = Profesor
        fields = "__all__"
    
class ProfesorAdmin(admin.ModelAdmin):
    forms = ProfesorFormsAdmin
    list_display = ('user', 'facultad','asignatura')




admin.site.register(Profesor,ProfesorAdmin)