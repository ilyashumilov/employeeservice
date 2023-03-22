from django.db import models
# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()
    position = models.CharField(max_length=100)
    compensation = models.IntegerField()
    age = models.IntegerField()
    dept = models.ForeignKey('Department', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + ' from  ' + str(self.dept)


class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return str(self.name)
