from rest_framework.response import Response
from .models import Employee, Department
from rest_framework.viewsets import ModelViewSet
from .serializers import EmployeeSerializer, DepartmentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.authentication import TokenAuthentication
from django.db.models import Count
import json

class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        TokenAuthentication,
    ]
    queryset = Employee.objects.all()
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        second_name_query = self.request.GET.get("second_name", None)
        dept_id_query = self.request.GET.get("dept_id", None)

        if second_name_query:
            self.queryset = self.queryset.filter(name__contains=second_name_query)
        if dept_id_query:
            self.queryset = self.queryset.filter(dept=dept_id_query)

        return self.queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="second_name",
                location=OpenApiParameter.QUERY,
                description="Parameter to filter by second name",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="dept_id",
                location=OpenApiParameter.QUERY,
                description="Parameter to filter by department id",
                required=False,
                type=str,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request)


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    pagination_class = None
    permission_classes = [
        AllowAny,
    ]
    authentication_classes = []
    queryset = Department.objects.annotate(part_employee_counter=Count("employee")) \
        .annotate(part_employee_compensation=Count("employee"))

    http_method_names = ["get"]


    def list(self, request, *args, **kwargs):
        employee_counter = sum([dept.part_employee_counter for dept in self.queryset])
        employee_compensation = sum([dept.part_employee_compensation for dept in self.queryset])

        to_return = {
            'employee_counter': employee_counter,
            'employee_compensation': employee_compensation,
            'departments': self.get_serializer(self.queryset, many=True).data
        }
        return Response(to_return)
