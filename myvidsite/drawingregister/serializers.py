from .models import *
from rest_framework import serializers

class DrawingSerializer(serializers.ModelSerializer):
	
	#For referencing in functions as fields
	# revitSheetNumber = serializers.ReadOnlyField() 
	# currentRev = serializers.ReadOnlyField()
	# nextRev = serializers.ReadOnlyField()
	# drawingNumber = serializers.ReadOnlyField()
	# drawingTitle = serializers.ReadOnlyField()
	# level = serializers.ReadOnlyField()
	# sequence = serializers.ReadOnlyField()

	#THIS CONVERTS THE STRINGIFIED DICTIONARY TO AN ACTUAL DICTIONARY
	data_store = serializers.JSONField()

	class Meta:
		model = Drawings
		fields = ('__all__')
		# read_only_fields = ['drawing_name',]

class SubmissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Submissions
		fields = ('__all__')