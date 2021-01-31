from django.db import models
import datetime


class Bus(models.Model):
    name = models.CharField(max_length=100)
    bus_model = models.CharField(max_length=100)
    year_of_prod = models.IntegerField(choices=[(i, str(i)) for i in range(1980, datetime.date.today().year + 1)])
    velocity = models.IntegerField()

    def __str__(self):
        return self.name + ' ' + self.bus_model


class Driver(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    bus = models.ManyToManyField(Bus)

    class Meta:
        ordering = ('surname', 'name',)

    def __str__(self):
        return self.name + ' ' + self.surname

    def age(self):
        today = datetime.date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < \
               (self.date_of_birth.month, self.date_of_birth.day))