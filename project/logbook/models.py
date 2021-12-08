from django.db import models
from django.template.defaultfilters import slugify


class Instrument(models.Model):
    name = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)
    mobile_campaign = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class InstrumentFile(models.Model):
    file = models.FileField(upload_to="files/instrument/")
    description = models.CharField(max_length=500)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.url

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super(InstrumentFile, self).delete(*args, **kwargs)
        storage.delete(path)


class Station(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    latitude = models.DecimalField(max_digits=11, decimal_places=6)
    longitude = models.DecimalField(max_digits=11, decimal_places=6)
    elevation = models.DecimalField(max_digits=4, decimal_places=0)
    instruments = models.ManyToManyField(Instrument, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class StationFile(models.Model):
    file = models.FileField(upload_to="files/station/")
    description = models.CharField(max_length=500)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.url

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super(StationFile, self).delete(*args, **kwargs)
        storage.delete(path)


class Campaign(models.Model):
    name = models.CharField(max_length=250, blank=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    date = models.DateField(help_text="Please use the following format: YYYY-MM-DD.", null=True)
    mobile_campaign = models.BooleanField(default=False)
    description = models.TextField(max_length=1000)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.station.name + " " + self.instrument.name + " " + str(self.date).replace('-', '')[:-2]
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class CampaignFile(models.Model):
    file = models.FileField(upload_to="files/campaign/")
    description = models.CharField(max_length=500)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.url

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super(CampaignFile, self).delete(*args, **kwargs)
        storage.delete(path)


class Flag(models.Model):
    flag = models.CharField(max_length=3)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.flag


class Logbook(models.Model):
    name = models.CharField(max_length=50)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = "Logbook " + self.campaign.name
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Event(models.Model):
    name = models.CharField(max_length=50, blank=True)
    logbook = models.ForeignKey(Logbook, on_delete=models.CASCADE)
    event_date = models.DateField(help_text="Please use the following format: YYYY-MM-DD.")
    description = models.TextField(max_length=1000)
    invalid_data = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    flags = models.ManyToManyField(Flag, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if Event.objects.filter(event_date=self.event_date).count() > 0:
            n = Event.objects.filter(event_date=self.event_date).count()
        else:
            n = 0
        self.name = self.logbook.name + " " + str(self.event_date) + " " + f"{n:02d}"
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


def event_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "files/event/%s.%s" % (instance.event.name, ext)
    return filename


class EventFile(models.Model):
    file = models.FileField(upload_to=event_file_path)
    description = models.CharField(max_length=500)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.url

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super(EventFile, self).delete(*args, **kwargs)
        storage.delete(path)
