from django import forms
from . import models

class ProblemImageForm(forms.ModelForm):
    class Meta:
        model = models.SolutionImage
        app_label = "solutions"
        verbose_name = "Картинка решения"
        verbose_name_plural = "Картинки решений"
        fields = "__all__"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(models.ProblemImage, self).save(*args, **kwargs)

class ProblemImageForm(forms.ModelForm):
    class Meta:
        model = models.ProblemImage
        app_label = "problems"
        verbose_name = "Картинка задачи"
        verbose_name_plural = "Картинки задач"
        fields = "__all__"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(models.ProblemImage, self).save(*args, **kwargs)

class ProblemForm(forms.ModelForm):
    class Meta:
        model = models.Problem
        app_label = "problems"
        verbose_name = "Задачи"
        verbose_name_plural = "Задача"
        fields = "__all__"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(models.Problem, self).save(*args, **kwargs)