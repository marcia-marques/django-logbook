from django.contrib import admin

from .models import Flag, Event, EventFile


class EventFileInline(admin.TabularInline):
    model = EventFile


class EventAdmin(admin.ModelAdmin):
    inlines = [
        EventFileInline,
    ]
    list_display = ('event_date', 'description')


admin.site.register(Flag)
admin.site.register(Event, EventAdmin)
admin.site.register(EventFile)
