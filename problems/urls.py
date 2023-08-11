from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "problems"

router = routers.DefaultRouter()
router.register(r'', views.ProblemViewSet)
router.register(r'problem_images', views.ProblemImageViewSet)
router.register(r'solution_images', views.SolutionImageViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
