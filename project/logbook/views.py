from django.views.generic import ListView
from django.http import HttpResponse
import csv

from .models import Campaign, Event


class HomeView(ListView):
    model = Campaign
    template_name = "logbook/home.html"
    context_object_name = 'campaigns'


def export_logbook_csv(request, slug):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format('logbook-' + slug + '.csv')

    writer = csv.writer(response)
    writer.writerow([
        'event_date', 'description', 'invalid', 'start_date', 'end_date', 'flags', 'revised'])

    events = Event.objects.filter(logbook__slug='logbook-' + slug).values_list(
        'event_date', 'description', 'invalid', 'start_date', 'end_date', 'flags__flag', 'revised')
    for event in events:
        writer.writerow(event)

    return response
