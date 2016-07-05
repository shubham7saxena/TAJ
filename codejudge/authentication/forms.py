from django.forms import ModelForm
from .models import *

class HackerForm(ModelForm):
	class Meta:
		model = Hacker
		fields = ['hackerName', 'email', 'password']