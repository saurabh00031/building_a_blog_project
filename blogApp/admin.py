from django.contrib import admin

# Register your models here.
from .models import Postinfo


@admin.register(Postinfo)
class PostDisp(admin.ModelAdmin):
    list_display=['id','title','desc']