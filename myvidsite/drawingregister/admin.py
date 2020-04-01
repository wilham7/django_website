from django.contrib import admin
from .models import *


class submissionInLine(admin.TabularInline):
	model = Submissions.req_drawings.through

class drawingAdmin(admin.ModelAdmin):



    # readonly_fields = ('drawingNumber', 'drawingTitle', 'level', 'sequence', 'currentRev', 'nextRev','drawing_name')

    # fieldsets = [
    #     ("Project", {'fields':["project",]}),
    #     ("Drawing Number sub-categories", {"fields": ["dn_project", "dn_originator", "dn_volume_system","dn_type", "dn_discipline", "dn_series","dn_level", "dn_zone_sequence"]}),
    #     ("Drawing title", {'fields': ["drawing_title1","drawing_title2","drawing_title3"]}),
    #     ("Additional info", {'fields': ["studio","model_location","revision_offset","scale","paper","dwg_type","discipline","phase","originator"]}),
    #     ("Generated", {'fields': ['drawingNumber', 'drawingTitle', 'level', 'sequence']}),
    #     ("Submissions", {'fields': ['currentRev', 'nextRev',]}),
    #     ("Data", {'fields': ['data_store',]}),

    # ]

    fields = ('project','data_store','drawing_name')

    inlines = [
        submissionInLine,
    ]

    list_per_page = 1000

class submissionAdmin(admin.ModelAdmin):
    
    readonly_fields = ('sub_dubspace','sub_nomatch','sub_incomplete',)

    filter_horizontal = ('req_drawings','sub_comp','was_submitted')

    fields = ('project','sub_date','file_path','req_drawings','sub_comp','sub_dubspace','sub_nomatch','sub_incomplete','was_submitted')
    # fieldsets = [
    #     ("To be Submitted", {'fields': ["to_be_submitted",]})
    # ]

    # inline = [
    #     submissionInLine,
    # ]
    # exclude = ('req_drawings',)

class projectAdmin(admin.ModelAdmin):
    fields = ('name','number','location')


# Register your models here.
admin.site.register(Drawings, drawingAdmin)
admin.site.register(Submissions, submissionAdmin)
admin.site.register(Projects)
