from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User, Group
from ckeditor.fields import RichTextField
# Create your models here.

class AuthUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(username=username, email=self.normalize_email(email),)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Hacker(AbstractBaseUser, PermissionsMixin):
    
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed.')
    ### Redefine the basic fields that would normally be defined in User ###
    username = models.CharField(unique=True, max_length=20, validators=[alphanumeric])
    email = models.EmailField(verbose_name='email address', unique=True, max_length=255)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    roll = models.CharField(max_length=20, null=False, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)
    attendace = models.PositiveSmallIntegerField(default = 0)
    ### Our own fields ###
    profileImage = models.ImageField(upload_to="avatar")
    objects = AuthUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def get_full_name(self):
        fullname = str(self.first_name) + " " + str(self.last_name)
        return fullname

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username