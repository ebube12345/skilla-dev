from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
#custom user model not default

class CustomUserManager(BaseUserManager):
#override create user method
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field required')
#clean up
        email = self.normalize_email(email) #meets required
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

#overide superuser
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('name', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('SuperUser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser must have is_superuser=True')
        
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    #manage allows to create a super user
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"


class AddressGlobal(models.Model):
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class UserProfile(models.Model):
    user = models.ForeignKey('CustomUser', related_name='user_profile', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pics")
    address_info = models.ForeignKey('AddressGlobal', related_name='user_address', null = True, on_delete=models.SET_NULL)
    dob = models.DateField()

    def __str__(self):
        return self.user.email