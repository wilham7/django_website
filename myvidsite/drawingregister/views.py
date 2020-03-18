from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
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

def postAconex(request, sub_date):
	sd = sub_date
	# val = Submissions.objects.get(sub_date=sd)


	sub = Submissions.objects.get(sub_date=sd)

	try:
		val = sub.for_submission_complete()
		print(val)
		sub.was_submitted = val
		print(sub)
		sub.save()

	except Exception as e:
		print(e)


	# sub = Submissions.objects.filter(sub_date=sd).update(was_submitted= val)


	# sub.was_submitted = sub.sub_comp
	# sub.save()
	# save = sub.sub_comp
	# sub.was_submitted = save



	return JsonResponse({'Test1':str(sub.was_submitted)})
	# sub.save()



def homepage(request):
	return render(request=request,
				  template_name="drawingregister/home.html",
				  context={})

def drawings(request):
	dwgs = Drawings.objects.all()


	return render(request=request,
				  template_name="drawingregister/drawings.html",
				  context={"context":dwgs})




# def single_drawing(request, single_slug):
# 	return render(request=request,
# 				  template_name="drawingregister/single_drawing.html",
# 				  context={"context":})



def single_submission(request, single_slug):

	subs = [c.sub_date for c in Submissions.objects.all()]

	if single_slug in subs:

		#Get all series that have the same tutorial_category 
		matching_sub = Submissions.objects.filter(sub_date=single_slug)
	


		return render(request=request,
				  	 template_name="drawingregister/single_submission.html",
				     context={"context":matching_sub})





def submissions(request):
	subs = Submissions.objects.all()


	return render(request=request,
				  template_name="drawingregister/submissions.html",
				  context={"context":subs})









def testing(request):
	drawings = [c.drawingNumber() for c in Drawings.objects.all()]
	# drawings = str(Drawings.objects.all())
	return JsonResponse({'Test1':drawings})
	

@csrf_exempt
# @csrf_protect
def updateDrawings(request):

	# data = '[{"id":"20", "dn_series":"11"},{"id":"21", "dn_series":"11"}]'

	log = []
	dn_to_return = []


	if request.method == "POST":

		try:
			createdcount = 0
			updatecount = 0
			
			# data = request.POST["data"]
			data = request.POST.get('data','')	

				# CHECK WHAT KEY AND VALUE IS COMING THROUGH
			# for key, value in request.POST.items():
			# 	print('Key: %s' % (key) ) 
			# 	print('Value %s' % (value) )

				#EXPLODE OUTER LAYER OF DICT
			jd = json.loads(data)
			jd = jd['data']

			log.append(jd)

			for drawing in jd:

				try:
					exist = get_object_or_404(Drawings, id=drawing['id'])
					# str_exist = str(exist)
					# print(str_exist)
					# dn_to_return.append(get_object_or_404(Drawings, id=drawing['id']))
					# print('2st checkpoint')
					# except:
					# 	dn_to_return.append("Didn't work lol")


					# exist = get_object_or_404(Drawings, pk=1)
					# log.append("hello" + str(exist))
					# log.append("Object exists")


					try:
						mod, created = Drawings.objects.update_or_create(id=drawing['id'], defaults=drawing)
						print("mod")
						print(mod)

						try:
							# updated = get_object_or_404(Drawings, id=drawing['id'])
							new = mod.drawing_name
							dn_to_return.append(new)
						except Exception as e:
							print(e)
								

						if created:
							createdcount += 1
						else:
							updatecount += 1
					except:
						log.append("update_or_create failed")

				except:
					log.append("Object doesn't exist")	

			print('A post')
			print(dn_to_return)
			return JsonResponse({'returns':dn_to_return})

		except:
			return JsonResponse({'Empty data?':''})

	else:

		print('Not a post')
		return JsonResponse({'test':"doesn't work"})





@csrf_exempt
def uploadDrawings(request):

	# data = '[{"dn_project":"BBB","dn_originator":"COX","dn_volume_system":"01","dn_type":"DR","dn_discipline":"AR","dn_series":"01","dn_level":"00","dn_zone_sequence":"~01","drawing_title1":"111111111111111111111111111111","drawing_title2":"STANDARD NOTES SYMBOLS & LEGEND","drawing_title3":"","studio":"Sydney","model_location":"Architecture","revision_offset":"","scale":"-","paper":"A2","dwg_type":"register","discipline":"Architectural","phase":"Design Development","originator":"Cox Architects"},{"dn_project":"SFS","dn_originator":"COX","dn_volume_system":"01","dn_type":"DR","dn_discipline":"AR","dn_series":"03","dn_level":"00","dn_zone_sequence":"~01","drawing_title1":"1234qwerasdf","drawing_title2":"STANDARD NOTES SYMBOLS & LEGEND","drawing_title3":"","studio":"Sydney","model_location":"Architecture","revision_offset":"","scale":"-","paper":"A0","dwg_type":"register","discipline":"Architectural","phase":"Design Development","originator":"Cox Architects"}]'
	
	log = []
	values = []


	if request.method == "POST":
		

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
					createdcount = createdcount+ 1
				else:
					updatecount = updatecount + 1
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