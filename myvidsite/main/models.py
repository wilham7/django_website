from django.db import models
from datetime import datetime



class TutorialCategory(models.Model):
	tutorial_category = models.CharField(max_length=200)
	category_summary = models.CharField(max_length=200)
	category_slug = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.tutorial_category


class TutorialSeries(models.Model):
	tutorial_series = models.CharField(max_length=200)
	tutorial_category = models.ForeignKey(TutorialCategory, null=True, default=1, verbose_name="Category", on_delete=models.SET_NULL)
	series_summary = models.CharField(max_length=200)
	series_order = models.IntegerField(blank=True, null=True, default=None)

	class Meta:
		verbose_name_plural = "Series"

	def __str__(self):
		return self.tutorial_series


# Create your models here.
class Tutorial(models.Model):
	tutorial_title = models.CharField(max_length=200)
	tutorial_content = models.TextField()
	tutorial_published = models.DateTimeField("date published", default=datetime.now())
	tutorial_slug = models.CharField(max_length=200, default="1")
	tutorial_series = models.ForeignKey(TutorialSeries, null=True, default=1, verbose_name="Series", on_delete=models.SET_NULL)	
	

	def __str__(self):
		return self.tutorial_title