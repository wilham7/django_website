from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def single_slug(request, single_slug):
	#Gets all fields from TutorialCategories and then just category_slug -> saved as a list called categories
	categories = [c.category_slug for c in TutorialCategory.objects.all()]
	#If the url typed in exists in the list of category_slug...
	if single_slug in categories:
		#Get all series that have the same tutorial_category 
		matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
		#Create dictionary
		series_urls = {}
		#Make sure all of the matching series are in correct order and then...
		for m in matching_series.order_by("series_order"):
			#We need to account for if a series has no tutorials in it -> This code tries to start on the first tut in the series, but if it doesn't have one, just pass over it
			try:
				#part_one = The title of the first published tutorial in that series
				part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_published")
				#Assigns a value to the keys in the dictionary. The keys are the series titles and the values are the slugs of the first published tutorials IN those series.
				series_urls[m] = part_one.tutorial_slug
			except:
				pass


		return render(request,
					  "main/category.html",
					  {"part_ones": series_urls})


#Setting up slugs for tutorials

	tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
	if single_slug in tutorials:
		this_tutorial = Tutorial.objects.get(tutorial_slug = single_slug)

		tutorials_from_series = Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by("tutorial_published")
		this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)

		return render(request,
					  "main/tutorial.html",
					  {"tutorial":this_tutorial,
					   "sidebar": tutorials_from_series,
					   "this_tutorial_idx": this_tutorial_idx})

	# return HttpResponse(f"{single_slug} does not correspond to anything.")
	return redirect('/dregister/')



def homepage(request):
	return render(request=request,
				  template_name="main/categories.html",
				  context={"categories": TutorialCategory.objects.all})

def register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"New Account Created: {username}")
			login(request, user)
			messages.info(request, f"You are now logged in as {username}")
			return redirect("main:homepage")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}: {form.error_messages[msg]}")


	form = UserCreationForm
	return render(request,
				  "main/register.html",
				  context={"form":form})