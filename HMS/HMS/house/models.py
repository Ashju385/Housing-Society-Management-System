from django.db import models
from django.conf import settings
from django.urls import reverse_lazy


# Create your models here.

class Service(models.Model):
    SERVICE_CATAGORIES = (
        ('Community Center', 'Community Center'),
        ('Picnic Spot', 'Picnic Spot'),
        ('Swimming Pool', 'Swimming Pool'),
        ('Transport Service', 'Transport Service'),
    )
    service_name = models.CharField(max_length=40, null=True)
    catagory = models.CharField(max_length=25, choices=SERVICE_CATAGORIES)
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.service_name} {self.catagory} for {self.capacity} people'


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    total_d = models.IntegerField(default=0)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user} has booked {self.service} from {self.check_in} to {self.check_out}'

    def get_service_catagory(self):
        service_catagories = dict(self.service.SERVICE_CATAGORIES)
        service_catagory = service_catagories.get(self.service.catagory)
        return service_catagory

    def get_cancel_booking_url(self):
        return reverse_lazy('house:CancelBookingView', args=[self.pk, ])
