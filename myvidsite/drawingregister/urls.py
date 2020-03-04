"""myvidsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf.urls import url, include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'drawings', views.DrawingViewSet)
router.register(r'submissions', views.SubmissionViewSet)

app_name = "drawingregister"

urlpatterns = [
	path("", views.homepage, name="homepage"),
	path("testing/", views.testing, name="testing"),
    path("uploadDrawings/", views.uploadDrawings, name="uploadDrawings"),
	path("uploadSubmissions/", views.uploadSubmissions, name="uploadSubmissions"),
    path("drawingTable/", views.drawingTable, name="drawingTable"), 
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
]
