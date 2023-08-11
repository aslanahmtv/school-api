from rest_framework import generics, permissions, viewsets, status
from rest_framework.pagination import LimitOffsetPagination

from . import serializers, models

class SolutionImageViewSet(viewsets.ModelViewSet):
    queryset = models.SolutionImage.objects.all()
    serializer_class = serializers.SolutionImageSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProblemImageViewSet(viewsets.ModelViewSet):
    queryset = models.ProblemImage.objects.all()
    serializer_class = serializers.ProblemImageSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = models.Problem.objects.all()
    serializer_class = serializers.ProblemSerializer

    def get_serializer_class(self):
        if 'fields' in self.request.query_params:
            fields = self.request.query_params['fields'].split(',')
            return type('ProblemSerializer', (serializers.ProblemSerializer,), {'Meta':
                type('Meta', (object,), {'model': models.Problem, 'fields': fields})})
        return serializers.ProblemSerializer