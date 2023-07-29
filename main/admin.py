from django.contrib import admin
from .models import Shelter, Opportunity
# Register your models here.
class ShelterAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone']

class OpportunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'species','age', 'gender', 'urgent', 'available']

admin.site.register(Shelter, ShelterAdmin)
admin.site.register(Opportunity, OpportunityAdmin)