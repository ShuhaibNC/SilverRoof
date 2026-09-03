from django.db import models

class Customer(models.Model):

    customer_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    location = models.CharField(max_length=150)
    gst = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.customer_name