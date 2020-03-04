from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from .models import *
from .serializers import *

import json

from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class DrawingViewSet(viewsets.ModelViewSet):
	queryset = Drawings.objects.all()
	serializer_class = DrawingSerializer
	filter_backends = [filters.SearchFilter ,DjangoFilterBackend]
	# filterset_fields = ['project__number',]
	search_fields = ('drawing_name',)

class SubmissionViewSet(viewsets.ModelViewSet):
	queryset = Drawings.objects.all()
	serializer_class = SubmissionSerializer
	filter_backends = [filters.SearchFilter ,DjangoFilterBackend]
	# filterset_fields = ['project__number',]
	search_fields = ('sub_date',)

# Create your views here.
def homepage(request):
	return JsonResponse({'key':'value'})


def testing(request):
	drawings = [c.drawingNumber() for c in Drawings.objects.all()]
	# drawings = str(Drawings.objects.all())
	return JsonResponse({'Test1':drawings})
	

@csrf_exempt
def uploadDrawings(request):

	# data = '[{"dn_project":"BBB","dn_originator":"COX","dn_volume_system":"01","dn_type":"DR","dn_discipline":"AR","dn_series":"01","dn_level":"00","dn_zone_sequence":"~01","drawing_title1":"111111111111111111111111111111","drawing_title2":"STANDARD NOTES SYMBOLS & LEGEND","drawing_title3":"","studio":"Sydney","model_location":"Architecture","revision_offset":"","scale":"-","paper":"A2","dwg_type":"register","discipline":"Architectural","phase":"Design Development","originator":"Cox Architects"},{"dn_project":"SFS","dn_originator":"COX","dn_volume_system":"01","dn_type":"DR","dn_discipline":"AR","dn_series":"03","dn_level":"00","dn_zone_sequence":"~01","drawing_title1":"1234qwerasdf","drawing_title2":"STANDARD NOTES SYMBOLS & LEGEND","drawing_title3":"","studio":"Sydney","model_location":"Architecture","revision_offset":"","scale":"-","paper":"A0","dwg_type":"register","discipline":"Architectural","phase":"Design Development","originator":"Cox Architects"}]'
	
	log = []
	values = []


	if request.method == "POST":
		
		# jd = json.loads(data)
		

		data = request.POST["data"]
		jd = json.loads(data)
		log.append(jd)
		# out = {"out": "working"}




		createdcount = 0
		updatecount = 0

		for drawing in jd:

			dnum = drawing['dn_project'] + "-" + drawing['dn_originator'] + "-" + drawing['dn_volume_system'] + "-" + drawing['dn_type'] + "-" + drawing['dn_discipline'] + drawing['dn_series'] + drawing['dn_level'] + drawing['dn_zone_sequence']
			dnum = str(dnum).replace("~","")	

			log.append(dnum)
			

			try:
				exist = get_object_or_404(Drawings, dn_project=drawing['dn_project'], dn_originator=drawing['dn_originator'], dn_volume_system= drawing['dn_volume_system'], dn_type=drawing['dn_type'], dn_discipline=drawing['dn_discipline'], dn_series=drawing['dn_series'], dn_level=drawing['dn_level'], dn_zone_sequence=drawing['dn_zone_sequence']) 
				# exist = get_object_or_404(Drawings, pk=1)
				log.append("hello" + str(exist))
				log.append("Object exists")
			except:
				log.append("Object doesn't exist")

			try:
				mod, created = Drawings.objects.update_or_create(dn_project=drawing['dn_project'], dn_originator=drawing['dn_originator'], dn_volume_system= drawing['dn_volume_system'], dn_type=drawing['dn_type'], dn_discipline=drawing['dn_discipline'], dn_series=drawing['dn_series'], dn_level=drawing['dn_level'], dn_zone_sequence=drawing['dn_zone_sequence'], defaults=drawing)
				# values = str(Drawings.objects.values())

				if created:
					createdcount += 1
				else:
					updatecount += 1
			except:
				log.append("update_or_create failed")


			return JsonResponse({'Created count':createdcount,'Updated count':updatecount})
			# return JsonResponse({'Log':log,'Created count':createdcount,'Objects':values})
	
	else:
		return JsonResponse({'Error':'ONLY POST REQUESTS'})


@csrf_exempt
def uploadSubmissions(request):

	# data = '[{"sub_date":"200214","req_drawings":["SFS-COX-01-DR-AR100005","SFS-COX-01-DR-AR100006"]}]'
	log = []

	createdcount = 0
	updatecount = 0

	if request.method == "POST": 
		

		data = request.POST["data"]
		jd = json.loads(data)
		log.append(jd)

		
		for sub in jd:

			try:
				#Updating
				try:
					exist = get_object_or_404(Submissions, sub_date=sub['sub_date']) 
					log.append("Object exists")


					mod, created = Submissions.objects.update_or_create(sub_date=sub['sub_date'])
					rd = sub['req_drawings']
					updatecount += 1

					try:
						exist.req_drawings.clear()
						for i in rd:
							dwg = Drawings.objects.get(drawing_name=i)
							# print(str(dwg))
							exist.req_drawings.add(dwg)
					except Exception as e:
						print(e)
				#Creating
				except:
					log.append("Object doesn't exist")
					mod, created = Submissions.objects.update_or_create(sub_date=sub['sub_date'])
					rd = sub['req_drawings']
					createdcount += 1

					try:
						exist.req_drawings.clear()
						for i in rd:
							dwg = Drawings.objects.get(drawing_name=i)
							print(str(dwg))
							exist.req_drawings.add(dwg)
					except Exception as e:
						print(e)

			except Exception as e:
				log.append(e)

		return JsonResponse({'Created count':createdcount,'Updated count':updatecount,'log':str(log)})

	else:
		return JsonResponse({'Error':'ONLY POST REQUESTS'})

def drawingTable(request):
	import json
	allDrawings = DrawingSerializer(Drawings.objects.all(), many=True).data
	context = {
	"data":json.dumps(allDrawings)
	}
	return render(request,"drawingregister/tabletest.html",context)