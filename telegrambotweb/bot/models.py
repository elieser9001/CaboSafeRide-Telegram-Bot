from ast import Delete
from django.db import models

class Documento(models.Model):
    descripción = models.CharField(max_length=80, null=False, blank=False, help_text="Descripción del documento")
    
    ruta_del_documento = models.FileField(
        upload_to="upload/files",
        help_text="Documento que va a mostrar el bot con algún comando vinculado"
    )
    
    def __str__(self):
        return str(self.descripción)
    
class Informacion(models.Model):
    título = models.CharField(max_length=80, null=False, blank=False, help_text="Título de la información")

    contenido = models.TextField(help_text="Contenido de la información que va a mostrar el bot con algún comando vinculado")

    def __str__(self):
        return str(self.título)

class Comando(models.Model):
    nombre = models.CharField(max_length=30, null=False, blank=False, help_text="Nombre del Documento")
    
    descripción = models.CharField(
        max_length=120,
        null=False,
        blank=False,
        default="Sin descripción",
        help_text="Descripción del comando a mostrar en la ayuda del bot"
    )
    
    documento = models.OneToOneField(
        Documento,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="Documento que va a retornar el bot con el comando"
    )
    
    información = models.OneToOneField(
        Informacion,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        help_text="Texto que va a mostrar el bot con el comando (sí no se establece un documento)"
    )

    def __str__(self):
        return str(self.nombre)
    
class UsuarioTelegram(models.Model):
    nombre = models.CharField(max_length=30, help_text="Nombre del usuario en telegram autorizado a usar el bot")
    
    usuario_telegram_id = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        help_text="ID del usuario en telegram autorizado a usar el bot"
    )
    
    def __str__(self):
        return str(self.nombre)

class Configuración(models.Model):
    usuario_telegram = models.ManyToManyField(UsuarioTelegram)

    def __str__(self):
        return "Configuración del Bot de Telegram"
