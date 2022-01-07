from django.shortcuts import render
from datetime import datetime, timedelta
import pandas as pd
import glob
import dask.dataframe as dd
import numpy as np

from logbook.models import Campaign
from logbook.models import Event

from .forms import (DataRaw24hFormFunction)
from .mygraphs import bokeh_raw


def graphs_raw_24h(request, slug):
    invalid = 0
    campaign = Campaign.objects.get(slug=slug)
    start_dates = Event.objects.filter(logbook__slug='logbook-' + slug, invalid=True).values_list('start_date')
    end_dates = Event.objects.filter(logbook__slug='logbook-' + slug, invalid=True).values_list('end_date')
    start_dates = [my_date[0] for my_date in list(start_dates)]
    end_dates = [my_date[0] for my_date in list(end_dates)]

    # form choices
    if campaign.raw_data_path:
        path = campaign.raw_data_path
        dirnames = glob.glob(path + '*/*/*')
        dirnames.sort(reverse=True)
        dates = list([filename[-10:] for filename in dirnames])
        date_choices = list(zip(dates, dates))

        # initial values
        days = dates[0]
        initial_data = {'days': days}

        # form
        raw_data_24h_form = DataRaw24hFormFunction(date_choices)
        form = raw_data_24h_form(request.POST or None, initial=initial_data)
        if form.is_valid():
            days = request.POST.get('days')
            if '_prev' in request.POST:
                days = (datetime.strptime(
                    days, '%Y/%m/%d') - timedelta(
                    days=1)).strftime('%Y/%m/%d')
                if days < date_choices[-1][0]:
                    days = date_choices[0][0]
                form = raw_data_24h_form(initial={'days': days})
            elif '_next' in request.POST:
                days = (datetime.strptime(
                    days, '%Y/%m/%d') + timedelta(
                    days=1)).strftime('%Y/%m/%d')
                if days > date_choices[0][0]:
                    days = date_choices[-1][0]
                form = raw_data_24h_form(initial={'days': days})
            elif '_invalid' in request.POST:
                invalid = 1

        # dataframe
        usecols = campaign.raw_var_list.split(',')
        dtype = campaign.raw_dtypes.split(',')
        dtype = dict(zip(usecols, dtype))
        filenames = [filename for filename in glob.iglob(
                path + days + '/*.dat')]
        filenames.sort()
        # ignoring last file as a temporary solution to broken line files
        # using "skipfooter" compromises the time of processing
        if days == dates[0]:
            filenames = filenames[:-1]
        if filenames:
            df = dd.read_csv(filenames,
                             sep=r'\s+',
                             usecols=usecols,
                             dtype=dtype,
                             engine='c',
                             )
            df = df.compute()
            df['DATE_TIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'])
            df = df.drop(['DATE', 'TIME'], axis=1)
            df = df[['DATE_TIME'] + [col for col in df.columns if col != 'DATE_TIME']]

            if invalid == 1:
                for start_date, end_date in zip(start_dates, end_dates):
                    df.loc[(df['DATE_TIME'] >= start_date.strftime("%Y-%m-%d %H:%M:%S")) &
                           (df['DATE_TIME'] <= end_date.strftime("%Y-%m-%d %H:%M:%S")), df.columns] = np.nan

            script, div = bokeh_raw(df, start_dates, end_dates)
            context = {'campaign': campaign,
                       'form': form,
                       'script': script, 'div': div}
            return render(request, 'dashboard/graphs_raw_24h.html', context)

        else:
            # form
            raw_data_24h_form = DataRaw24hFormFunction([('', 'no data available')])
            form = raw_data_24h_form(request.POST or None)
            context = {'campaign': campaign, 'form': form}
            return render(request, 'dashboard/graphs_raw_24h.html', context)

    else:
        context = {'campaign': campaign}
        return render(request, 'dashboard/graphs_raw_24h.html', context)
