from django.contrib import admin
from .models import *
# Register your models here.
class Csvadmin(admin.ModelAdmin):
    list_display =['image_name','objects_detected','Image']


admin.site.register(CSVData,Csvadmin)