from django.contrib import admin

from .models import Flag, Event, EventFile, EventImage


class EventFileInline(admin.TabularInline):
    model = EventFile


class EventImageInline(admin.TabularInline):
    model = EventImage


class EventAdmin(admin.ModelAdmin):
    inlines = [
        EventFileInline,
        EventImageInline,
    ]
    readonly_fields = ('author', 'created_on', 'updated_on')

    def save_model(self, request, obj, form, change):
        obj.author = request.user.first_name + ' ' + request.user.last_name
        obj.save()


admin.site.register(Flag)
admin.site.register(Event, EventAdmin)
admin.site.register(EventFile)
