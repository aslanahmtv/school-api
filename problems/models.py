from django.db import models
from django.core.validators import FileExtensionValidator

class Problem(models.Model):

    SUBJECTS = (
        ("physics", "Физика",),
        ("math", "Математика",),
    )

    text = models.CharField(max_length=255, null=True, blank=True)
    grade = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    subject = models.CharField(max_length=255, choices=SUBJECTS, blank=True, null=True)
    solution = models.CharField(max_length=255, blank=True, null=True)

class ProblemSubmission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, blank=True, null=True)
    answer_text = models.CharField(max_length=255, null=True, blank=True)
    answer_value = models.FloatField(blank=True, null=True)
    solution_image = models.FileField(
        null=True, blank=True,
        upload_to='media/problem_submissions/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'img', 'jpg', 'jpeg'])]
    )

class ProblemImage(models.Model):
    image = models.ImageField(upload_to="media/problem_images/")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, blank=True, null=True)

class SolutionImage(models.Model):
    image = models.ImageField(upload_to="media/solution_images/")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, blank=True, null=True)