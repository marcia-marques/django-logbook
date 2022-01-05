from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Instrument, InstrumentFile,\
                    Station, StationFile,\
                    Campaign, CampaignFile,\
                    Flag, \
                    Event, EventFile,\
                    Logbook


class InstrumentFileInline(admin.TabularInline):
    model = InstrumentFile


class InstrumentAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    inlines = [InstrumentFileInline]


class StationFileInline(admin.TabularInline):
    model = StationFile


class StationAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    inlines = [StationFileInline]


class CampaignFileInline(admin.TabularInline):
    model = CampaignFile


class CampaignAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'slug',)
    inlines = [CampaignFileInline]


class EventFileInline(admin.TabularInline):
    model = EventFile


class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'slug',)
    list_display = ('name', 'event_date', 'description', 'invalid', 'start_date', 'end_date', 'flags', 'revised')
    fields = ['logbook', 'event_date', 'description', 'invalid', 'start_date', 'end_date', 'flags', 'revised']
    list_filter = ('logbook', 'event_date', 'invalid', 'revised', 'flags')
    inlines = [EventFileInline]

    class Media:
        js = ('/static/admin/js/hide_attribute.js',)


class EventInline(admin.TabularInline):
    model = Event
    fields = ['event_date', 'description', 'invalid', 'start_date', 'end_date', 'flags', 'revised']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 40})},
    }
    show_change_link = True


class LogbookAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'slug',)
    inlines = [EventInline]


admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Flag)
admin.site.register(Event, EventAdmin)
admin.site.register(EventFile)
admin.site.register(Logbook, LogbookAdmin)
