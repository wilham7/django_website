from django import forms

from .models import *





class SubmissionsForm(forms.ModelForm):
	class Meta:
		model = Submissions
		fields = ['file_path']