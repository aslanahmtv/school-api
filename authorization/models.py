from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and saves a new user"""
        if not email:
            raise ValueError('The Email field is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        default_group = Group.objects.filter(name="UserFree")
        if default_group.exists():
            user.groups.add(default_group)
        return user

    def create_superuser(self, email, password):
        """Create and saves a new superuser"""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    verification_str = models.CharField(max_length=255, null=True, blank=True)
    activation_date = models.DateTimeField(null=True, blank=True)
    default_grade = models.IntegerField(null=True, blank=True)

    viewed_problems = models.JSONField(default=list, blank=True, null=True)
    viewed_problems_solutions = models.JSONField(default=list, blank=True, null=True)
    saved_problems = models.JSONField(default=list, blank=True, null=True)
    solved_problems = models.JSONField(default=list, blank=True, null=True)

    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'