from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Problem)
admin.site.register(models.ProblemSubmission)
admin.site.register(models.ProblemImage)
admin.site.register(models.SolutionImage)