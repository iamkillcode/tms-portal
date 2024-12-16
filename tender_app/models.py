from django.db import models

class TenderTracker(models.Model):
    year = models.IntegerField()
    procurement_type = models.CharField(max_length=10)
    last_sequence = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.year} - {self.procurement_type} - {self.last_sequence}"


class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.code