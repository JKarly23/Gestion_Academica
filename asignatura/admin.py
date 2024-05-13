from django import forms
from django.contrib import admin

from asignatura.models import Asignatura, ComentarioAsignatura,Nota

# Register your models here.
class ComentarioFormsAdmin(forms.ModelForm):

    class Meta:
        model = ComentarioAsignatura
        fields = "__all__"
    
class ComentarioAdmin(admin.ModelAdmin):
    
    forms = ComentarioFormsAdmin
    list_display = ["tema","estudiante","asignatura"]



class AsignaturaFormsAdmin(forms.ModelForm):

    class Meta:
        model = Asignatura
        fields = "__all__"

class AsignaturaAdmin(admin.ModelAdmin):

    forms = AsignaturaFormsAdmin
    list_display = ["name","profesor"]    



class NotasAdminForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = '__all__'

class NotasAdmin(admin.ModelAdmin):
    form = NotasAdminForm
    list_display = ('estudiante', 'asignatura', 'nota')



admin.site.register(ComentarioAsignatura,ComentarioAdmin)
admin.site.register(Asignatura,AsignaturaAdmin)
admin.site.register(Nota, NotasAdmin)