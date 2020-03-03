from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from .models import *

import json


# Create your views here.
def homepage(request):
	return JsonResponse({'key':'value'})


def testing(request):
	drawings = [c.drawingNumber() for c in Drawings.objects.all()]
	# drawings = str(Drawings.objects.all())
	return JsonResponse({'Test1':drawings})
	


def upload(request):

	data = '[{"dn_project":"SFS","dn_originator":"COX","dn_volume_system":"01","dn_type":"DR","dn_discipline":"AR","dn_series":"01","dn_level":"00","dn_zone_sequence":"~01","drawing_title1":"0000000000000000000000000000000000000000000000","drawing_title2":"STANDARD NOTES SYMBOLS & LEGEND","drawing_title3":"","studio":"Sydney","model_location":"Architecture","revision_offset":"","scale":"-","paper":"A0","dwg_type":"register","discipline":"Architectural","phase":"Design Development","originator":"Cox Architects"},{"dn_project":"SFS","dn_originator":"COX","dn_volume_system":"01","dn_type":"DR","dn_discipline":"AR","dn_series":"03","dn_level":"00","dn_zone_sequence":"~01","drawing_title1":"1234qwerasdf","drawing_title2":"STANDARD NOTES SYMBOLS & LEGEND","drawing_title3":"","studio":"Sydney","model_location":"Architecture","revision_offset":"","scale":"-","paper":"A0","dwg_type":"register","discipline":"Architectural","phase":"Design Development","originator":"Cox Architects"}]'
	
	log = []
	values = []


	if request.method == "POST":
		pass

	else:
		jd = json.loads(data)
		createdcount = 0

		for drawing in jd:

			dnum = drawing['dn_project'] + "-" + drawing['dn_originator'] + "-" + drawing['dn_volume_system'] + "-" + drawing['dn_type'] + "-" + drawing['dn_discipline'] + drawing['dn_series'] + drawing['dn_level'] + drawing['dn_zone_sequence']
			dnum = str(dnum).replace("~","")	

			log.append(dnum)
			

		try:
			exist = get_object_or_404(Drawings, dn_project=drawing['dn_project'], dn_originator=drawing['dn_originator'], dn_volume_system= drawing['dn_volume_system'], dn_type=drawing['dn_type'], dn_discipline=drawing['dn_discipline'], dn_series=drawing['dn_series'], dn_level=drawing['dn_level'], dn_zone_sequence=drawing['dn_zone_sequence']) 
		except:
			log.append("Object doesn't exist")

		try:
			mod, created = Drawings.objects.update_or_create(dn_project=drawing['dn_project'], dn_originator=drawing['dn_originator'], dn_volume_system= drawing['dn_volume_system'], dn_type=drawing['dn_type'], dn_discipline=drawing['dn_discipline'], dn_series=drawing['dn_series'], dn_level=drawing['dn_level'], dn_zone_sequence=drawing['dn_zone_sequence'], defaults=drawing)
			values = str(Drawings.objects.values())

			if created:
				createdcount += 0
				log.append(createdcount)
			else:
				log.append("Updated not created")

		except:
			log.append("update_or_create failed")


		return JsonResponse({'Log':log,'Created count':createdcount,'Objects':values})