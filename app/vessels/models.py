from django.db import models

class Vessel(models.Model):
    code = models.CharField(max_length=5, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Equipment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active"
        INACTIVE = "inactive"

    vessel = models.ForeignKey(Vessel,related_name='equipments', on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=8, unique=True)
    location = models.CharField(max_length=60)
    status =  models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)