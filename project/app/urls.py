from django.urls import path
from rest_framework import routers
from .views import EmployeeViewSet, DepartmentViewSet
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


router = routers.SimpleRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'departments', DepartmentViewSet)
urlpatterns = router.urls

urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
]