from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def homepage(request):
	return JsonResponse({'key':'value'})
	