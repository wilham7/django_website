from django import forms
from django.forms import modelform_factory, ModelForm

from .models import *





class SubmissionsForm(forms.ModelForm):
	class Meta:
		model = Submissions
		fields = ['file_path']


class NewDwgForm(forms.ModelForm):

	#Getting the reverse of the many2many field. It is filtered out in the view
	submissions = forms.ModelMultipleChoiceField(Submissions.objects.all())
	class Meta:
		model = Drawings
		# fields = ['project','dn_project','dn_originator','dn_volume_system','dn_type','dn_discipline','dn_series','dn_level','dn_zone_sequence','drawing_title1','drawing_title2','drawing_title3','studio','model_location','revision_offset','scale','paper','dwg_type','discipline','phase','originator',
		# 'submissions',

		# ]
		fields = ['data_store']
		widgets = {'project': forms.HiddenInput()}

	#This is some function that saves the special reverse m2m field 
	def save(self, *args, **kwargs):
		instance = super(NewDwgForm, self).save(*args, **kwargs)
		# instance.submissions.add(self.cleaned_data['submissions'])
		instance.submissions.set(self.cleaned_data['submissions'])

		#This has to run to make sure the drawing number gets generated after the form is made!!!
		instance.drawingNumber()
		instance.save()
		return instance


class NewSubForm(forms.ModelForm):
	class Meta:
		model = Submissions
		fields = ['sub_date','req_drawings','project']
		labels = {
			'sub_date':('Submission Date')
		}
		help_texts = {
			'sub_date':('This should be in the format of... Year(XX), Month(XX), Day(XX)')
		}

		widgets = {'project': forms.HiddenInput(),
				   

		}
  #           'sub_date': Charfield(attrs={'cols': 80, 'rows': 20}),
  #       }
