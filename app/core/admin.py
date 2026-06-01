from  django.contrib import admin
from .models import Parque, ImagenParque, Reservacion, Usuario, Hospedaje

admin.site.register(Parque)
admin.site.register(ImagenParque)
admin.site.register(Reservacion)
admin.site.register(Usuario)
admin.site.register(Hospedaje)