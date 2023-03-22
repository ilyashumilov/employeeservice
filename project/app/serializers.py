from rest_framework import serializers
from .models import Employee, Department


class EmployeeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=100)
    image = serializers.ImageField()
    position = serializers.CharField(max_length=100)
    compensation = serializers.IntegerField()
    age = serializers.IntegerField()
    dept = serializers.CharField(max_length=100)

    def create(self, data):
        dept_id = data.pop('dept')
        data['dept'] = Department.objects.get(id=dept_id)
        return Employee.objects.create(**data)


class DepartmentSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=100)
    manager = EmployeeSerializer()
