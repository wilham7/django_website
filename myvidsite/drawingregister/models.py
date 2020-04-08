from django.db import models
from django.core.files import File
from os import listdir
from django.forms import ModelForm
from django import forms
import ast
import os, sys
import os.path
# from os.path import isfile, join 



location_choices = (
	('Sydney','Sydney'),
	('Melborune','Melborune'),
	('Perth','Perth'),
	('Brisbane','Brisbane'),
	('Canberra','Canberra'),
	('Adelaide','Adelaide'),
	('International','International'),
)

scale_choices = (
	('-','-'),
	('1','1'),
	('2','2'),
	('5','5'),
	('10','10'),
	('20','20'),
	('50','50'),
	('100','100'),
	('200','200'),
	('500','500'),
	('1000','1000'),
	('2000','2000'),
)

paper_choices = (
	('A0','A0'),
 	('A1','A1'),   
	('A2','A2'),   
	('A3','A3'),   
	('A4','A4'),   
)

type_choices = (
	("2D Drawing","2D Drawing"),
	("2D Model","2D Model"),
	("3D Model","3D Model"),
	("Animation File","Animation File"),
	("Calculation","Calculation"),
	("Certificate","Certificate"),
	("Clash Report","Clash Report"),
	("Combined Model","Combined Model"),
	("Correspondence","Correspondence"),
	("Cost Plan","Cost Plan"),
	("Database","Database"),
	("Drawing","Drawing"),
	("File Note","File Note"),
	("Information Exchange File","Information Exchange File"),
	("Material Sample","Material Sample"),
	("Matrix","Matrix"),
	("Meeting Minutes","Meeting Minutes"),
	("Model Rendition File","Model Rendition File"),
	("Presentation","Presentation"),
	("Programme","Programme"),
	("Register","Register"),
	("Report","Report"),
	("Room Data Sheet","Room Data Sheet"),
	("Schedule","Schedule"),
	("Specification","Specification"),
	("Survey","Survey"),
	("Visualisation","Visualisation"),
)

phase_choices = (
	("Design Development","Design Development"),
)


level_LUT = {"00":"00 - Datum","B1":"B1 - Lower Basement","L0":"L0 - Basement","L1":"L1 - Concourse","L1M":"L1M - Concourse Mezzanine","L2":"L2 - Level 2","L3":"L3 - Level 3","L4":"L4 - Level 4","L5":"L5 - Level 5","RF":"RF - Roof","XX":"XX - Level NA","ZZ":"ZZ - Multiple Level","LT":"ZZ - Multiple Level","MT":"ZZ - Multiple Level","ST":"ZZ - Multiple Level","UT":"ZZ - Multiple Level"}
sequence_LUT = {"00":"00 - Whole Site","00.":"00 - Whole Site","01":"01 - Building Zone A","02":"02 - Building Zone B","03":"03 - Building Zone C","04":"04 - Building Zone D","05":"05 - Building Zone E","06":"06 - Building Zone F","07":"07 - Building Zone G","08":"08 - Building Zone H","09":"09 - Building Zone I","11":"11 - Building Sector 1","12":"12 - Building Sector 2","13":"13 - Building Sector 3","14":"14 - Building Sector 4","15":"15 - Building Sector 5","16":"16 - Building Sector 6","17":"17 - Building Sector 7","18":"18 - Building Sector 8","19":"19 - Building Sector 9","20":"20 - Building Sector 10","21":"21 - Building Sector 11","22":"22 - Building Sector 12","23":"23 - Building Sector 13","24":"24 - Building Sector 14","25":"25 - Building Sector 15","26":"26 - Building Sector 16","27":"27 - Building Sector 17","28":"28 - Building Sector 18","29":"29 - Building Sector 19","30":"30 - Building Sector 20","31":"31 - Building Sector 21","32":"32 - Building Sector 22","33":"33 - Building Sector 23","34":"34 - Building Sector 24"}


##LOOK UP TABLES
##________________________________________________
discipline_to_xx = {"Architectural":"AR"}
originator_to_cox = {"COX Architects":"COX"}
##________________________________________________

##ANDREW'S SCRIPT FOR MAKING DICTIONARIES IN DATAFIELDS
class DataFieldFormField(forms.CharField):
    def prepare_value(self, value):
        try:
            import json
            if value =="{}":
                return value
            else:
                return json.dumps(value)
        except Exception as e:
            return value

class DataField(models.TextField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 9999
        kwargs['default'] = {}
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)
    def parseString(self, s):
        import json
        try:
            ns = json.loads(s)
            return ns
        except Exception as e:
            return {}
    def from_db_value(self, value, expression, connection):
        if value is None:
            return {}
        return self.parseString(value)
    def to_python(self, value):
        try:
            py_val = self.parseString(value)
            return py_val
        except Exception as e:
            return {}
    def get_db_prep_save(self, value, connection):
        import json
        try:
            new_value = json.dumps(value)
            return json.dumps(value)
        except Exception as e:
            return json.dumps({"error":str(e)})
    def formfield(self, **kwargs):
        defaults = {'form_class': DataFieldFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
class parentModel(models.Model):
    data = DataField()

##ANDREW'S NEW SAVE FUNCTION
def save( self, *args, **kw ):
	self.checkGeneralTitle()
	super( staff, self ).save( *args, **kw )

# Create your models here.
class Projects(models.Model):

	name = models.CharField(max_length=200)
	number = models.CharField(max_length=200, unique=True)
	location = models.CharField(max_length=200,choices=location_choices)
	namingConv = models.TextField(max_length=9999, default="[]")
	namingLUTs = models.TextField(max_length=9999, default="[]")

	class Meta:
		ordering = ['number']
		verbose_name_plural = "Projects"

	def __str__(self):
	    return str(self.number+" - "+self.name)

class Drawings(models.Model):
	# drawing_title1 = models.CharField(max_length=200,default="Architectural Services")
	# drawing_title2 = models.CharField(max_length=200)
	# drawing_title3 = models.CharField(max_length=200,blank=True,null=True)
	# studio = models.CharField(max_length=200,choices=location_choices,default="Sydney")
	# model_location = models.CharField(max_length=200,blank=True,null=True)
	# revision_offset = models.CharField(max_length=200,blank=True,null=True)
	# scale = models.CharField(max_length=200,choices=scale_choices,default="100")
	# paper = models.CharField(max_length=200,choices=paper_choices,default="A0")
	# dwg_type = models.CharField(max_length=200,choices=type_choices,default="2D Drawing")
	# phase = models.CharField(max_length=200,choices=phase_choices,default="Design Development")

	project = models.ForeignKey(Projects, on_delete=models.CASCADE,blank=True,null=True)
	data_store = DataField()
	drawing_name = models.CharField(max_length=200,default="", blank=True)


	def drawingName(self):
		dname = []
		nConv = self.project.namingConv
		nConv = ast.literal_eval(nConv)
		for part in nConv:
			if part in self.data_store:
				dname.append(self.data_store.get(part))
			else:
				dname.append(part)

			#USING THE LOOK UP TABLES
		luts = self.project.namingLUTs
		luts = ast.literal_eval(luts)
		for t in luts:
			LUT_dname = []
			lutdict = eval(t)
			for n in dname:
				if n in lutdict:
					new = lutdict.get(n)
					LUT_dname.append(new)
				else:
					LUT_dname.append(n)
			dname = LUT_dname

			#TURNING THE ARRAY INTO A STRING
		dname = "".join(dname)
			#REMOVING THE ~ ... THIS MAY NOT BE REQUIRED ON ALL JOBS
		dname = dname.replace("~","")

		self.drawing_name = dname
		self.save()
		return dname



	# def currentRev(self):
	# 	cr = self.submissions.all().count()
	# 	return cr

	# def nextRev(self):
	# 	cr = self.submissions.all().count() + 1
	# 	return cr		


	# def revitSheetNumber(self):
	# 	rsn = self.dn_discipline + self.dn_series + self.dn_level + self.dn_zone_sequence
	# 	rsn = str(rsn).replace("~","")
	# 	return rsn

	# def drawingNumber(self):
	# 	dn = self.dn_project + "-" + self.dn_originator + "-" + self.dn_volume_system + "-" + self.dn_type + "-" + self.revitSheetNumber()
	# 	dn = str(dn).replace("~","")
	# 	self.drawing_name = dn
	# 	self.save()
	# 	return dn

	# def drawingNumber(self):
	# 	dn = "placeholder" + "-" + str(self.pk) 
	# 	# dn = str(dn).replace("~","")
	# 	self.drawing_name = dn
	# 	self.save()
	# 	return dn

	# def drawingTitle(self):
	# 	if self.drawing_title3 == "" or self.drawing_title3 == "-":
	# 		dt = self.drawing_title2
	# 	else:
	# 		try:
	# 			dt = self.drawing_title2 + "-" + self.drawing_title3
	# 		except:
	# 			dt = self.drawing_title2
	# 	return dt

	# def level(self):
	# 	try:
	# 		lvl = level_LUT[self.dn_level]
	# 	except:
	# 		lvl = "Null"
	# 	return lvl

	# def sequence(self):
	# 	try:
	# 		if "~" in str(self.dn_zone_sequence):
	# 			sq = "01-99 - Default Sequence"
	# 		else:
	# 			sq = sequence_LUT[self.dn_zone_sequence]
	# 	except:
	# 		sq = "Not a valid zone_sequence"
	# 	return sq

	class Meta:
		verbose_name_plural = "Drawings"
	def __str__(self):
		if self.drawing_name != "":
			return self.drawing_name
		else:
			return ("placeholder" + "-" + str(self.pk))


class Submissions(models.Model):
	sub_date = models.IntegerField()
	file_path = models.CharField(max_length=500,default="", blank=True)

	req_drawings = models.ManyToManyField('Drawings', blank=True, related_name='submissions')
	project = models.ForeignKey(Projects, on_delete=models.CASCADE)

	was_submitted = models.ManyToManyField('Drawings', blank=True, related_name='submissions_was_sub')


	# FILE IS CORRECT
	sub_comp = models.ManyToManyField('Drawings', blank=True, related_name='submissions_comp')
	# HAS DOUBLE SPACES
	sub_dubspace = models.CharField(max_length=5000,default="", blank=True)
	# WAS IN THE FOLDER BUT HAS NO CORRESPONDING FILES
	sub_nomatch = models.CharField(max_length=5000,default="", blank=True)
	# IN ORIGINAL LIST -> NOT FOUND
	sub_incomplete = models.CharField(max_length=5000,default="", blank=True)

	def for_submission_complete(self):
		#Drawing names as a list
		dn = []
		#Get files
		gf = []
		#Get files split
		gf_all = []
		gf_dubspace = []

		#Set to defaults at the start
		self.sub_dubspace = []
		self.sub_comp.clear()
		self.sub_nomatch = []
		self.sub_incomplete = []

		try:
			gf = os.listdir(self.file_path)
			try:
				for f in gf:
					#Removing the file type
					gf_suffix = f.split(".")[-1]
					gf_all.append(f.replace("."+gf_suffix,""))
			except Exception as e:
				print(e)
		except:
			return "This is not a valid directory"
		

		gf_clean = gf_all
		for f in gf_clean:
			if "  " in f:
				gf_clean.remove(f)
				gf_dubspace.append(f)
		gf_dubspace = list(gf_dubspace)
		self.sub_dubspace = gf_dubspace 


		dnames = self.req_drawings.all()
		for d in dnames:
			dn.append(d.drawing_name)

		#Checking for matches
		gf_matches = set(dn) & set(gf_clean)
		gf_matches = list(gf_matches)

		to_add = self.req_drawings.filter(drawing_name__in=gf_matches)
		self.sub_comp.set(to_add)

		gf_notmatches = set(gf_clean) - set(dn)
		gf_notmatches = list(gf_notmatches) 
		self.sub_nomatch = gf_notmatches


		gf_notfound =  set(dn) - set(gf_clean) 
		gf_notfound = list(gf_notfound) 
		self.sub_incomplete = gf_notfound


		self.save()
		return gf_all


	def __str__(self):
	    return (str(self.project)+" - "+str(self.sub_date))

	class Meta:
		verbose_name_plural = "Submissions"
		unique_together = ('sub_date', 'project')
