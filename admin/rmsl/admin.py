from django.contrib import admin

# Register your models here.
from rmsl.models import Resource, Event

admin.site.register(Resource)
admin.site.register(Event)
