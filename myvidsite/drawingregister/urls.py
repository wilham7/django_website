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
router.register(r'drawings_set', views.DrawingViewSet)
router.register(r'submissions_set', views.SubmissionViewSet)

app_name = "drawingregister"

urlpatterns = [
	path("", views.home, name="home"),
    path("<pj_slug>/drawings/", views.drawings, name="drawings"),
    path("drawings/<str:single_slug>/", views.single_drawing, name="single_drawing"),
    path("<pj_slug>/submissions/", views.submissions, name="submissions"),
    path("submissions/<str:single_slug>/", views.single_submission, name="single_submission"),
    path("submissions/open_file_path/<str:file_path>/", views.open_file_path, name="open_file_path"),

    path("latest_dwg/", views.latest_dwg, name="latest_dwg"),
    path("latest_sub/", views.latest_sub, name="latest_sub"),
    path("<pj_slug>/transmittal/", views.transmittal, name="transmittal"),
    path("<pj_slug>/newsub/", views.newsub, name="newsub"),
    path("<pj_slug>/newdwg/", views.newdwg, name="newdwg"),



    path("postAconex/<str:sub_date>/", views.postAconex, name="postAconex"),
    path("uploadDrawings/", views.uploadDrawings, name="uploadDrawings"),
    path("updateDrawings/", views.updateDrawings, name="updateDrawings"),
	path("uploadSubmissions/", views.uploadSubmissions, name="uploadSubmissions"),
    path("drawingTable/", views.drawingTable, name="drawingTable"), 


    path("newView/", views.newView, name="newView"),
    path("dictTest/", views.dictTest, name="dictTest"),

    #This url redirects all single strings to home!!
    path("<str:pj_slug>/", views.single_project, name="single_project"),



    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
]
