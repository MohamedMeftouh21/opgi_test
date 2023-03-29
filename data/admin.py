from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import wilaya,Unite,Cite,Batiment,Contrat,Occupant,Logement,Consultation,Service_contentieux
    
class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
                pass    
    
admin.site.register(wilaya, BlogAdmin) 
admin.site.register(Unite) 
admin.site.register(Cite) 
admin.site.register(Batiment) 
admin.site.register(Contrat) 
admin.site.register(Occupant) 
admin.site.register(Logement) 
admin.site.register(Consultation)
admin.site.register(Service_contentieux)
