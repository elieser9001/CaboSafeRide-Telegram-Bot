from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Documento, UsuarioTelegram, Información, Comando, Configuración

admin.site.unregister(Group)
admin.site.register(Documento)
admin.site.register(Información)
admin.site.register(Comando)
admin.site.register(UsuarioTelegram)
admin.site.register(Configuración)