from django.db import models


# Create your models here.
class AdharCard(models.Model):
    number = models.CharField(max_length=10, unique=True, null=False)

    def __str__(self):
        return self.number


class Designation(models.Model):
    title = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.title


class Cources(models.Model):
    cource_name = models.CharField(max_length=50)

    def __str__(self):
        return self.cource_name


class Person(models.Model):
    name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    dob = models.DateField(null=False)

    adhar_number = models.OneToOneField(
        AdharCard, related_name="adhar_card", on_delete=models.CASCADE, primary_key=True
    )
    designation = models.ForeignKey(
        Designation, on_delete=models.DO_NOTHING, related_name="designation", null=True
    )
    cources = models.ManyToManyField(Cources, related_name="cources")

    def __str__(self):
        return self.name
