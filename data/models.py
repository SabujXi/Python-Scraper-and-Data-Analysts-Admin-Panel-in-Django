from django.db import models
# Create your models here.


class DataModel(models.Model):
    active_no = models.CharField(max_length=256, db_index=True, verbose_name="Number", null=True)
    city_data_not_found = models.BooleanField(default=False)
    city = models.CharField(max_length=256, db_index=True, verbose_name="City",  null=False)
    name = models.CharField(max_length=256,  default="")
    dba = models.CharField(max_length=256,  default="")
    phone = models.CharField(max_length=256, default="")
    carrier_type = models.CharField(max_length=256, default="")
    active_trucks = models.IntegerField(default=-1)
    mailing_address = models.CharField(max_length=256, default="")
    effective_date = models.CharField(max_length=256, default="")

    #
    checked_manually = models.BooleanField(default=False)
    record_url = models.URLField()  # According to active no


class DifferentDataModel(DataModel):
    """
    When the data scraping app is rerun and then this one is filled up
    But whatever this one provide it will not mess with manually checked Data
    """
