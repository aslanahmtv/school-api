from rest_framework import serializers

from . import models

class SolutionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SolutionImage
        fields = "__all__"

class ProblemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProblemImage
        fields = "__all__"

class ProblemSerializer(serializers.ModelSerializer):
    problem_images = serializers.SerializerMethodField()
    solution_images = serializers.SerializerMethodField()

    class Meta:
        model = models.Problem
        fields = "__all__"
    
    def get_problem_images(self, problem):
        # Get all ProblemImages related to the problem
        problem_images = problem.problemimage_set.all()
        # Serialize the related ProblemImages
        serializer = ProblemImageSerializer(problem_images, many=True, context=self.context)
        return serializer.data
    
    def get_solution_images(self, problem):
        # Get all ProblemImages related to the problem
        solution_images = problem.solutionimage_set.all()
        # Serialize the related ProblemImages
        serializer = SolutionImageSerializer(solution_images, many=True, context=self.context)
        return serializer.data