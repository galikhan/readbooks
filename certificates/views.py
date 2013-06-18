# Create your views here.
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from certificates.models import KatevProductionStudentsInfo as Students, TurkishCertificates, EnglishCertificates, TurkishLevel, EnglishLevel,CertificateLinks
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime, simplejson, readbooks.settings as settings
from django.contrib.auth.decorators import login_required
import readbooks.settings as s

@login_required
def cert_list( request, school ):
	cl = CertificateLinks.objects.filter(school=school)
	school = school_id_converter(school)	
	lessons = ["computer", "english", "turkish"]
#	return HttpResponse(s.HOME_PATH)

	return render(request, "download.html", {"certificates":cl, "lessons":lessons, "school":school} )

@login_required
def list_computer(request):

	school = request.session.__getitem__("school")
	school = school_id_converter(school)	
	students = Students.objects.using('katev').filter( school_id = school, class_field = 11 )
	lessons = ["computer", "english", "turkish"]

	return render(request, "studentlist.html",{ "students": students , "lessons": lessons, "type":"computer","school":school })

@login_required
def list_english(request):

	school = request.session.__getitem__("school")
	school = school_id_converter(school)	
	students = Students.objects.using('katev').filter( school_id = school , class_field = 11 )
	level = EnglishLevel.objects.all()
	certified = 0
	for student in students:
		try:
			slevels = EnglishCertificates.objects.get(student = student.student_id)
			certified +=1
			student.knowledgelevel = slevels.level.id
		except EnglishCertificates.DoesNotExist:
			student.knowledgelevel = 0
			pass	

	lessons = ["computer", "english", "turkish"]
	return render(request, "studentlist.html",{ "students": students , "lessons": lessons, "type":"english", "level":level,"certified":certified,"school":school })

@login_required
def list_turkish(request):

	school = request.session.__getitem__("school")
	school = school_id_converter(school)	
	level = TurkishLevel.objects.all()
	students = Students.objects.using('katev').filter( school_id = school , class_field = 11 )

	certified = 0
	for student in students:
		try:
			slevels = TurkishCertificates.objects.get(student = student.student_id)
			student.knowledgelevel = slevels.level.id
			certified +=1
		except TurkishCertificates.DoesNotExist:
			student.level = 0
			pass	

	lessons = ["computer", "english", "turkish"]
	return render(request, "studentlist.html",{ "students": students , "lessons": lessons, "type":"turkish" , "level":level,"certified":certified ,"school":school})


def set_level(request):

	if request.is_ajax():
		lang_type = request.POST["type"]
		student = request.POST["student-id"]
		level = request.POST["level"]

		if lang_type == "english":
			levelObject = EnglishLevel.objects.get(id = level)
			try:
				obj = EnglishCertificates.objects.get( student=student )
			except EnglishCertificates.DoesNotExist:	
				obj = EnglishCertificates()
			obj.student = student				
			obj.level = levelObject
			obj.save()

		elif lang_type == "turkish":	
			levelObject = TurkishLevel.objects.get(id = level)
			try:
				obj = TurkishCertificates.objects.get( student=student )
			except TurkishCertificates.DoesNotExist:	
				obj = TurkishCertificates()
			obj.student = student				
			obj.level = levelObject
			obj.save()

	json = simplejson.dumps({ "success":"true" })
	return HttpResponse(json, "application/json")


@login_required
def print_computer(request):

	school = request.session.__getitem__("school")
	school = school_id_converter(school)	
	date = str(datetime.datetime.now().date())
	name = "computer-"+school+"-"+date+".pdf"

	students = Students.objects.using('katev').filter( school_id = school, class_field = 11 )
	path = settings.MEDIA_ROOT+"certificates/"+name
	c = canvas.Canvas( path, pagesize = A4 )
	heigth, width = A4

	for student in students:
		full_name = str(student.en_name.encode("utf8") +" "+ student.en_surname.encode("utf8"))
		c.drawImage( settings.HOME_PATH + "/images/computer.jpg",0,0, heigth, width)
		c.drawString(320, 338, full_name)
		c.drawString(85, 453, str(student.student_id)+"1")
		c.drawString(85, 438, date)
		c.showPage()
	c.save()	
	save_link(school, name, "computer")
	school = request.session.__getitem__("school")
	return HttpResponseRedirect(reverse("cert_list", args={school}))

@login_required
def print_turkish(request):

	school = request.session.__getitem__("school")
	school = school_id_converter(school)	
	date = str(datetime.datetime.now().date())

	name = "tukish-"+school+"-"+date+".pdf"

	students = Students.objects.using('katev').filter( school_id = school, class_field = 11 )
	studentid = []
	for student in students:
		studentid.append(student.student_id)

	slevels = TurkishCertificates.objects.filter(student__in = studentid)
	student_levels = {}

	for slevel in slevels:
		student_levels[slevel.student] = slevel.level.name

	path = settings.MEDIA_ROOT+"certificates/"+name
	c = canvas.Canvas( path, pagesize = A4 )
	heigth, width = A4

	for student in students:
		try:
			level_cerficate = str(student_levels[student.student_id]).lower()
			full_name = str(student.en_name.encode("utf8") +" "+ student.en_surname.encode("utf8"))
			cert_name = "/images/"+level_cerficate+".jpg"
			c.drawImage( settings.HOME_PATH + cert_name,0,0, heigth, width)
			c.drawString(250, 340, full_name)
			c.drawString(85, 453, str(student.student_id)+"3")
			c.drawString(85, 438, date)
			c.showPage()
		except KeyError:
			pass
				
	c.save()	
	save_link(school, name, "turkish")
	school = request.session.__getitem__("school")
	return HttpResponseRedirect(reverse("cert_list", args={school}))

@login_required
def print_english(request):

	school = request.session.__getitem__("school")
	school = school_id_converter(school)	
	date = str(datetime.datetime.now().date())

	name = "english-"+school+"-"+date+".pdf"


	students = Students.objects.using('katev').filter( school_id = school, class_field = 11 )
	studentid = []
	for student in students:
		studentid.append(student.student_id)

	slevels = EnglishCertificates.objects.filter(student__in = studentid)
	student_levels = {}


	for slevel in slevels:
		student_levels[slevel.student] = slevel.level.name

	path = settings.MEDIA_ROOT+"certificates/"+name
	c = canvas.Canvas( path, pagesize = A4 )
	heigth, width = A4

	for student in students:
		try:
			level_cerficate = str(student_levels[student.student_id]).lower()
			full_name = student.en_name.encode("utf8") +" "+ student.en_surname.encode("utf8")
			cert_name = "/images/"+level_cerficate+".jpg"
			c.drawImage( settings.HOME_PATH + cert_name,0,0, heigth, width)
			c.setFont('Vera', 25)
			c.drawString(300, 340, full_name)
			c.setFont('Vera', 20)
			c.drawString(85, 453, str(student.student_id)+"2")
			c.drawString(85, 438, date)
			c.showPage()
		except KeyError:
			pass
				
	c.save()	
	save_link(school, name, "english")

	school = request.session.__getitem__("school")
	return HttpResponseRedirect(reverse("cert_list", args={school}))

@login_required
def update_name_surname(request):

	if request.is_ajax():
		name_surname = request.POST['name-surname']
		student_id = request.POST["student-id"]
		massive = []
		massive = student_id.split("-")
		sid = massive[1]
		info_type = massive[0]

		try:
			students = Students.objects.using('katev').get( student_id = sid )
			if info_type == "name":
				students.en_name = name_surname
			else:	
				students.en_surname = name_surname
		except Students.DoesNotExist:
			pass	

	json = simplejson.dumps({ "name_surname":students.en_name+" "+students.en_surname })
	return HttpResponse(json, "application/json")

def save_link(school, name, cert_type):

	try:
		cl = CertificateLinks.objects.get( school = school, certificate_type = cert_type)
	except CertificateLinks.DoesNotExist:	
		cl = CertificateLinks()
		cl.school = school
		cl.name = name
		cl.certificate_type = cert_type
	cl.save()
	
	return school

def school_id_converter(school_id):

	school_id = str(school_id)
	slen = len(school_id)
	if slen == 1:
		school_id = "00"+school_id
	elif slen == 2:
		school_id = "0"+school_id

	return school_id		
