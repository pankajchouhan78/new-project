from django.db import models


# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subjects(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, null=True)
    sub_name = models.CharField(max_length=50)

    def __str__(self):
        return self.sub_name


class student(models.Model):
    name = models.CharField(max_length=50)
    # teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, null=True)
    subjects = models.ManyToManyField(Subjects, blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    genders = (("M", "male"), ("F", "female"))
    eid = models.AutoField(primary_key=True)
    ename = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=genders)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    profile = models.ImageField(upload_to="profile")
    dob = models.DateField(null=False)

    def __str__(self):
        return self.ename
