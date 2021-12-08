from django.contrib import admin

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
    inlines = [EventFileInline]


class EventInline(admin.TabularInline):
    model = Event


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
