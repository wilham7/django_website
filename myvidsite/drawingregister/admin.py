from django.contrib import admin
from .models import *


class submissionInLine(admin.TabularInline):
	model = Submissions.req_drawings.through

class drawingAdmin(admin.ModelAdmin):
    readonly_fields = ('revitSheetNumber', 'drawingNumber', 'drawingTitle', 'level', 'sequence', 'currentRev', 'nextRev', 'reqSubmissions','drawing_name')

    fieldsets = [
        ("Drawing Number sub-categories", {"fields": ["dn_project", "dn_originator", "dn_volume_system","dn_type", "dn_discipline", "dn_series","dn_level", "dn_zone_sequence"]}),
        ("Drawing title", {'fields': ["drawing_title1","drawing_title2","drawing_title3"]}),
        ("Additional info", {'fields': ["studio","model_location","revision_offset","scale","paper","dwg_type","discipline","phase","originator"]}),
        ("Generated", {'fields': ['revitSheetNumber', 'drawingNumber', 'drawingTitle', 'level', 'sequence']}),
        ("Submissions", {'fields': ['reqSubmissions', 'currentRev', 'nextRev',]}),
        # ("test", {'fields': ['drawing_name']}),
    ]

    inlines = [
        submissionInLine,
    ]

class submissionAdmin(admin.ModelAdmin):
    filter_horizontal = ('req_drawings',)
    # inline = [
    #     submissionInLine,
    # ]
    # exclude = ('req_drawings',)



# Register your models here.
admin.site.register(Drawings, drawingAdmin)
admin.site.register(Submissions, submissionAdmin)
