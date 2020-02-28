from django.contrib import admin
from .models import *


class drawingAdmin(admin.ModelAdmin):
    readonly_fields = ('revitSheetNumber', 'drawingNumber', 'drawingTitle', 'level', 'sequence', )



# Register your models here.
admin.site.register(Drawings, drawingAdmin)
