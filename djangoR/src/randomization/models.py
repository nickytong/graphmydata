from django.db import models
from jsonfield import JSONField

# Create your models here.
class SimpleRandomization(models.Model):
    N = models.IntegerField(null=False)
    seed = models.IntegerField()
    date_created = models.DateField()
    # store list field as json
    result = JSONField()
