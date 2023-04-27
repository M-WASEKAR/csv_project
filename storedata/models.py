from django.db import models

# Create your models here.
from django.db import models

class CSVData(models.Model):
    image_name = models.CharField(max_length=255)
    objects_detected = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    Image = models.ImageField(upload_to='images/')