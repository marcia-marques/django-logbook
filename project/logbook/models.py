from django.db import models


class Flag(models.Model):
    flag = models.CharField(max_length=3)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.flag


class Event(models.Model):
    event_date = models.DateField(help_text="Please use the following format: YYYY-MM-DD.")
    description = models.TextField(max_length=1000)
    invalid_data = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    flags = models.ManyToManyField(Flag, blank=True)

    def __str__(self):
        return self.description


class EventFile(models.Model):
    file = models.FileField(upload_to="logbook/files/")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.url

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super(EventFile, self).delete(*args, **kwargs)
        storage.delete(path)
