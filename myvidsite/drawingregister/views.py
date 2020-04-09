from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.contrib import messages
from .models import *
from .serializers import *
from .forms import *

import datetime
import ast
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


def newView(request):
	objs = Drawings.objects.all()
	for d in objs:
		d.originator = 'Cox Architects'
		d.save()
		d.drawingName()
	return JsonResponse({"Status":"Drawing names updated"})

def dictTest(request):
	dwg = Drawings.objects.get(drawing_name="SFS-COX-01-DR-AR24L402")
	dwgdict = dwg.data_store
	return JsonResponse({"test":dwgdict})





def postAconex(request, sub_date):

	sub = Submissions.objects.get(sub_date=sub_date)

	try:
		val = sub.sub_comp.all()
		sub.was_submitted.set(val)
		sub.save()
		print("Updating worked")

	except Exception as e:
		print(e)
# return HttpResponse(status=204)
	return redirect('/dregister/submissions/'+str(sub))

def latest_dwg(request):

	latest_d = Drawings.objects.order_by('id')
	latest_d = latest_d.reverse()
	latest_d = latest_d[0]
	latest_d = str(latest_d)

	return redirect('/dregister/drawings/'+latest_d)

def latest_sub(request):

	latest_d = Submissions.objects.order_by('id')
	latest_d = latest_d.reverse()
	latest_d = latest_d[0]
	latest_d = str(latest_d)

	return redirect('/dregister/submissions/'+latest_d)



def newsub(request, pj_slug):
	
	pj_name = Projects.objects.get(number=pj_slug)
	#Setting initial values for the form - has to match the project of the slug
	initial_data = {
		'project':pj_name,
		}
	form = NewSubForm(request.POST or None, initial=initial_data)
	#Need to filter the drawing queryset by the project number
	form.fields["req_drawings"].queryset = Drawings.objects.filter(project__number = pj_slug)

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			messages.success(request, f"New Submission Created!", extra_tags='successSub')
			return HttpResponseRedirect(reverse('drawingregister:newsub', args=[pj_slug]))
		else:
			messages.error(request, f"This Submission Already Exist")

	return render(request=request,
			  	 template_name="drawingregister/newsub.html",
			     context={"form":form,"pj_name":pj_name})

def newdwg(request, pj_slug):
	
	pj_name = Projects.objects.get(number=pj_slug)
	#Setting initial values for the form - has to match the project of the slug
	initial_data = {
		'project':pj_name,
		}
	form = NewDwgForm(request.POST or None, initial=initial_data)
	#Need to filter the submissions queryset by the project number..
	#This only works because the queryset was built within the form since it is a reverse m2m
	form.fields["submissions"].queryset = Submissions.objects.filter(project__number = pj_slug)

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			messages.success(request, f"New Drawing Created!", extra_tags='successDwg')
			return HttpResponseRedirect(reverse('drawingregister:newdwg', args=[pj_slug]))

	return render(request=request,
			  	 template_name="drawingregister/newdwg.html",
			     context={"form":form,"pj_name":pj_name})



def single_submission(request, single_slug):

	# subs = [c.sub_date for c in Submissions.objects.all()]
	subs = Submissions.objects.all()
	subs = list(map(str, subs))

	sd = single_slug.split(" ")[-1]
	pjn = single_slug.split(" ")[0]

	if single_slug in subs:

		matching_sub = Submissions.objects.get(sub_date=sd, project__number=pjn)

		# FORM
		form = SubmissionsForm(request.POST or None, instance=matching_sub)
		if form.is_valid():
			form.save()

		sub_dwgs = matching_sub.req_drawings.all()
		#Run the function in the model to update values
		matching_sub.for_submission_complete()

		if matching_sub.sub_comp == "":
			sub_comp = ""
		else:
			sub_comp = matching_sub.sub_comp.all()

		if matching_sub.sub_dubspace == []:
			sub_dubspace = []
		else:
			sub_dubspace = matching_sub.sub_dubspace

		if matching_sub.sub_nomatch == []:
			sub_nomatch = []
		else:
			sub_nomatch = matching_sub.sub_nomatch

		if matching_sub.was_submitted == "":
			was_sub = ""
		else:
			was_sub = matching_sub.was_submitted.all()

		# #Sub_comp is coming in as a string that looks like a list so it must be converted into a real list
		# try:
		# 	sub_comp = ast.literal_eval(sub_comp)
		# except: 
		# 	pass
		# try:
		# 	was_sub = ast.literal_eval(was_sub)
		# except:
		# 	pass

		year = sd[0:2]
		year = "20"+year
		month = sd[2:4]
		if month[0] == "0":
			month = month[1]
		try:	
			mydate = datetime.datetime.strptime(month, '%m')
			month = mydate.strftime('%B')
		except:
			pass
		day = sd[4:6]

		return render(request=request,
				  	 template_name="drawingregister/single_submission.html",
				     context={"form":form,"submission":matching_sub,"sub_dwgs":sub_dwgs,"sub_comp":sub_comp,"was_sub":was_sub,"sub_dubspace":sub_dubspace,"sub_nomatch":sub_nomatch,"year":year,"month":month,"day":day,})

	return HttpResponse(f"{single_slug} couldn't be found in the database.")

def single_drawing(request, single_slug):

	dwgs = [c.drawing_name for c in Drawings.objects.all()]
	dwgs = list(map(str, dwgs))

	if single_slug in dwgs:
		matching_dwg = Drawings.objects.get(drawing_name=single_slug)

		#Getting the other direction of the manytomany field
		req_subs = matching_dwg.submissions.all()
		return render(request=request,
					  template_name="drawingregister/single_drawing.html",
					  context={"this_dwg":matching_dwg,"req_subs":req_subs})
	else:
		return HttpResponse(f"{single_slug} couldn't be found in the database.")

def transmittal(request, pj_slug):
	dwgs = Drawings.objects.filter(project__number = pj_slug)
	dname = [d.drawing_name for d in Drawings.objects.filter(project__number = pj_slug)]
	dname = list(map(str, dname))
	subs = Submissions.objects.filter(project__number = pj_slug)
	sname = [s.sub_date for s in Submissions.objects.filter(project__number = pj_slug)]
	sname.sort()

	mylist = []
	# y=0
	for d in dwgs:
		x=0
		sublist = []
		# sublist.append(dname[y])
		# y += 1
		ds = [x.sub_date for x in d.submissions.all()]
		try:
			for s in sname:
				if s in ds:
					x += 1
					sublist.append(x)
				else:
					sublist.append(0)
		except:
			for s in sname:
				sublist.append(0)
		mylist.append(sublist)

	return render(request=request,
				  template_name="drawingregister/transmittal.html",
				  context={"dwgs":dwgs,"subs":subs,"dname":dname,"sname":sname,"mylist":mylist})

def home(request):
	pjs = Projects.objects.all()
	return render(request=request,
				  template_name="drawingregister/home.html",
				  context={"pjs":pjs})	

def single_project(request, pj_slug):

	pj_numbers = [p.number for p in Projects.objects.all()]
	if pj_slug in pj_numbers:
		pj = Projects.objects.get(number=pj_slug)
		return render(request=request,
					  template_name="drawingregister/single_project.html",
					  context={"number":pj_slug,"pj":pj})	
	else:
		return redirect('/dregister/')

def open_file_path(request, file_path):

	try:
		path = file_path
		path = os.path.realpath(file_path)
		os.startfile(path)
	except Exception as e:
		path = os.path.realpath("C:/")

		os.startfile(path)
	return HttpResponse(status=204)

def drawings(request, pj_slug):
	dwgs = Drawings.objects.filter(project__number = pj_slug)
	return render(request=request,
				  template_name="drawingregister/drawings.html",
				  context={"context":dwgs,"pj_slug":pj_slug})

def submissions(request, pj_slug):
	subs = Submissions.objects.filter(project__number = pj_slug)
	return render(request=request,
				  template_name="drawingregister/submissions.html",
				  context={"context":subs,"pj_slug":pj_slug})

@csrf_exempt
# @csrf_protect
def updateDrawings(request):


	data_to_return = [] 


	if request.method == "POST":
		data = request.POST['data']
		data = ast.literal_eval(data)
		data = data.get("data")


		for obj in data:
			dwg = Drawings.objects.get(pk=obj.get("id"))
			old_data = dwg.data_store
			new_data = obj.get("data_store")
			combined_data = {}
			combined_data.update(old_data)
			try:
				combined_data.update(new_data)
			except Exception as e:
				print(e)

			if combined_data == old_data:
				pass
				print("No changes to update")
			else:
				dwg.data_store = combined_data
				dwg.drawingName()
				dwg.save()
				print("A Drawing was updated!")
				print(dwg.drawing_name)

				data_dict  = {"id":dwg.id,"drawing_name":dwg.drawing_name}
				data_to_return.append(data_dict)

				print(data_to_return)


	return JsonResponse({"updatedData":data_to_return})


@csrf_exempt
def uploadDrawings(request):

	# data = '[{"dn_project":"BBB","dn_originator":"COX","dn_volume_system":"01","dn_type":"DR","dn_discipline":"AR","dn_series":"01","dn_level":"00","dn_zone_sequence":"~01","drawing_title1":"111111111111111111111111111111","drawing_title2":"STANDARD NOTES SYMBOLS & LEGEND","drawing_title3":"","studio":"Sydney","model_location":"Architecture","revision_offset":"","scale":"-","paper":"A2","dwg_type":"register","discipline":"Architectural","phase":"Design Development","originator":"Cox Architects"},{"dn_project":"SFS","dn_originator":"COX","dn_volume_system":"01","dn_type":"DR","dn_discipline":"AR","dn_series":"03","dn_level":"00","dn_zone_sequence":"~01","drawing_title1":"1234qwerasdf","drawing_title2":"STANDARD NOTES SYMBOLS & LEGEND","drawing_title3":"","studio":"Sydney","model_location":"Architecture","revision_offset":"","scale":"-","paper":"A0","dwg_type":"register","discipline":"Architectural","phase":"Design Development","originator":"Cox Architects"}]'
	log = []
	values = []
	if request.method == "POST":
		data = request.POST["big_data"]
		jd = json.loads(data)
		createdcount = 0
		updatecount = 0

		pj = Projects.objects.get(number='218018.00')

		for d in jd:
			data = d["data"]
			# print(d)
			try:
				Drawings.objects.create(data_store=data,project=pj)
				updatecount += 1
				print("Create count:" + str(updatecount))
			except Exception as e:
				print(e)			


		return JsonResponse({'Upload status':success})


	# 	for drawing in jd:

	# 		dnum = drawing['dn_project'] + "-" + drawing['dn_originator'] + "-" + drawing['dn_volume_system'] + "-" + drawing['dn_type'] + "-" + drawing['dn_discipline'] + drawing['dn_series'] + drawing['dn_level'] + drawing['dn_zone_sequence']
	# 		dnum = str(dnum).replace("~","")	

	# 		log.append(dnum)
			

	# 		try:
	# 			exist = get_object_or_404(Drawings, dn_project=drawing['dn_project'], dn_originator=drawing['dn_originator'], dn_volume_system= drawing['dn_volume_system'], dn_type=drawing['dn_type'], dn_discipline=drawing['dn_discipline'], dn_series=drawing['dn_series'], dn_level=drawing['dn_level'], dn_zone_sequence=drawing['dn_zone_sequence']) 
	# 			# exist = get_object_or_404(Drawings, pk=1)
	# 			log.append("hello" + str(exist))
	# 			log.append("Object exists")
	# 		except:
	# 			log.append("Object doesn't exist")

	# 		try:
	# 			mod, created = Drawings.objects.update_or_create(dn_project=drawing['dn_project'], dn_originator=drawing['dn_originator'], dn_volume_system= drawing['dn_volume_system'], dn_type=drawing['dn_type'], dn_discipline=drawing['dn_discipline'], dn_series=drawing['dn_series'], dn_level=drawing['dn_level'], dn_zone_sequence=drawing['dn_zone_sequence'], defaults=drawing)
	# 			# values = str(Drawings.objects.values())

	# 			if created:
	# 				createdcount = createdcount+ 1
	# 			else:
	# 				updatecount = updatecount + 1
	# 		except:
	# 			log.append("update_or_create failed")


	# 		return JsonResponse({'Created count':createdcount,'Updated count':updatecount})
	# 		# return JsonResponse({'Log':log,'Created count':createdcount,'Objects':values})
	
	# else:
	# 	return JsonResponse({'Error':'ONLY POST REQUESTS'})

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
					pj = Projects.objects.get(number='218018.00')


					log.append("Object doesn't exist")

					Submissions.objects.create(sub_date=sub['sub_date'], project=pj)
					exist = get_object_or_404(Submissions, sub_date=sub['sub_date'])

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

	tableHeads = {}

	allDwg = Drawings.objects.all()[:100]
	for d in allDwg:
		ddict = d.data_store
		for k in ddict:
			if k in tableHeads:
				pass
			else:
				tableHeads["data_store."+k] = (str(k).capitalize()).replace("_"," ") 

	# Get regular fields
	baseTableHeads = {}
	fields = [f.get_attname() for f in Drawings._meta.fields]
	for f in fields:
		if f != 'data_store':
			baseTableHeads[f] = (str(f).capitalize()).replace("_"," ") 

	starts_with = ["id","drawing_name"]
	params_filter = ["project_id"]

	all_params = tableHeads
	all_params.update(baseTableHeads)

	start_params = {}
	end_params = {}

	for i in all_params:
		if i in starts_with:
			start_params[i] = all_params[i]
		else:
			end_params[i] = all_params[i]

	params = sorted(end_params.items(), key=lambda item: item[1].lower())

	final_params = {}
	final_params.update(start_params)
	final_params.update(end_params)


	allDrawings = DrawingSerializer(allDwg, many=True).data
	context = {
	"params":final_params,"base_params":baseTableHeads,"params_filter":params_filter,"data":json.dumps(allDrawings)
	}

	return render(request,"drawingregister/drawing_table.html",context)


	# return JsonResponse({"Test":str(context)})


	# allDrawings = DrawingSerializer(Drawings.objects.all(), many=True).data
	# context = {
	# "data":json.dumps(allDrawings)
	# }

