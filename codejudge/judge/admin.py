from django.contrib import admin
from judge.models import *

# Register your models here.
admin.site.register(Problem)
admin.site.register(Contest)
admin.site.register(Language)
admin.site.register(Solution)