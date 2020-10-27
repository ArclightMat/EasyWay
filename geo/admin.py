from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import User, AccessibleLocal, Rank

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Rank)
@admin.register(AccessibleLocal)
class AccessibleLocalAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')