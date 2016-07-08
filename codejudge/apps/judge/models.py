from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User, Group
from ckeditor.fields import RichTextField
from apps.authentication.models import Hacker
from taggit.managers import TaggableManager

class Contest(models.Model):
    contestName = models.CharField(max_length=200, unique=True, null=False)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

    def __unicode__(self):
        return self.contestName

class Problem(models.Model):
    contest = models.ForeignKey(Contest)
    problemSetter = models.CharField(max_length=200)
    problemTitle = models.CharField(max_length=200)
    problemStatement = RichTextField(config_name='awesome_ckeditor')
    testInput = models.FileField(upload_to='testInput')
    testOutput = models.FileField(upload_to='testOutput')
    timeLimit = models.PositiveSmallIntegerField()
    languagesAllowed = models.CommaSeparatedIntegerField(max_length=200)
    inputFormat = RichTextField(config_name='awesome_ckeditor')
    outputFormat = RichTextField(config_name='awesome_ckeditor')
    constraints = RichTextField(config_name='awesome_ckeditor')
    sampleInput = RichTextField(config_name='awesome_ckeditor')
    sampleOutput = RichTextField(config_name='awesome_ckeditor')
    solvedBy = models.PositiveSmallIntegerField(default=0)
    #tags for problems
    tags = TaggableManager()
    
    def __unicode__(self):
        return self.problemTitle

class Language(models.Model):
    language = models.CharField(max_length=30, default="C")
    extension = models.CharField(max_length=10)

    def __unicode__(self):
       return self.language

class Solution(models.Model):
    hacker = models.ForeignKey(Hacker)
    contest = models.ForeignKey(Contest)
    problem = models.ForeignKey(Problem)
    solution = models.FileField(upload_to='solution')
    attempts = models.PositiveSmallIntegerField()
    language = models.ForeignKey(Language)
    time = models.DecimalField(max_digits=2, decimal_places=2)
    status = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return str(self.id)
