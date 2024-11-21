from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL


class RoleChoice(models.TextChoices):
    ADMIN = 'admin', "Admin"
    USER = 'user', 'User'
    SUPERVISOR = 'supervisor', "Super Visor"
    MANAGER = 'manager', "Manager"
    EMPLOYEE = 'employee', "Employee"
    REP = 'rep', "Reporter"
    CUSTOMER = 'customer', "Customer"
    CREDIT_CARD_HOLDER = 'credit_card_holder', "Credit Cardholder"
    SUPERVISOR_EMPLOYEE = 'supervisor_employee', "Supervisor"



class Role(models.Model):
    name = models.CharField(max_length=100, choices=RoleChoice.choices, default=RoleChoice.EMPLOYEE, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise ValidationError("Name should only contain alphabetical characters.")
        return name
    


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # You can add custom fields here
    role = models.ForeignKey('Role', on_delete=models.CASCADE,  related_name='users', null=True, blank=True)  # Adding the roles field

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use email for login instead of username
    REQUIRED_FIELDS = ['username']  # Fields required for creating a superuser

    def __str__(self):
        return self.email
    

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@example.com'):
            raise ValidationError("Email must end with '@example.com'")
        return email
    



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE,  related_name='users_profile', null=True, blank=True)  # Adding the roles field


    def __str__(self):
        return self.user.username
