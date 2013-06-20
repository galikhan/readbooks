from django.utils.translation import ugettext as _
from models import *
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.http import HttpResponse,HttpResponseRedirect, Http404 
from django.contrib.auth.models import User
from forms import *
from django.db.models import Q
from statistics.models import *
from django.conf import settings

def import_all(request):
		
	teachers = KatevProductionTeacherInfo.objects.using('katev').all()
	counter = 0
	for t in teachers:
		try:
			teacher = TeacherProfile.objects.get(teacher_numeric_id = t.teacher_numeric_id)
			teacher.pas = t.pas
			counter+=1
		except TeacherProfile.DoesNotExist:
			teacher = TeacherProfile()
			teacher.kz_name = t.kz_name
			teacher.kz_surname = t.kz_surname
			teacher.teacher_numeric_id = t.teacher_numeric_id
			teacher.teacher_id = t.teacher_id
			teacher.school_id = t.school_id
			teacher.school_numeric_id = t.school_numeric_id
			teacher.pas = t.pas
			teacher.gorev_short = t.gorev_short
			teacher.branch_id = t.branch_id
			pass	
		teacher.save()

#	students = KatevProductionStudentsInfo.objects.using('katev').all()

#	for s in students:

#		studens = StudentProfile()
#		studens.kz_name = s.kz_name
#		studens.kz_surname = s.kz_surname
#		studens.student_id = s.student_id
#		studens.school_id = s.school_id
#		studens.password = s.password
#		studens.class_field = s.class_field
#		studens.division = s.division
#		studens.gender = s.gender
#		studens.save()
	
	
					
	return render_to_response('test.html', {'teacher': counter},)

def import_branch(request):

	branches = Branch.objects.using("katev").all()
	for branch in branches:
		newbranch = Branch()
		newbranch.name = branch.name
		newbranch.general_name = branch.general_name
		newbranch.kz_general_name = branch.kz_general_name
		newbranch.tr_general_name = branch.tr_general_name
		newbranch.ru_general_name = branch.ru_general_name
		newbranch.short_name = branch.short_name
		newbranch.save()
					
	return render_to_response('test.html', {'teachers': ""},)

def create_users(request):
	
#IMPORtANT	
	counter = 0
	teachers = TeacherProfile.objects.all()
	for t in teachers:
		counter +=1
		user = User.objects.get_or_create(username ='ktl'+t.teacher_id)
		user.set_password(t.pas)
		user.save()
#

	users = OldUsers.objects.using('katev').all()

	for u in users:
		try:
			user = User.objects.get(username =u.username)
			if user is not None:
				if u.email is not None:
					user.email = u.email
					user.save()

		except User.DoesNotExist:
			pass


	return render_to_response('test.html', { "teacher":counter },)

def viewallbooks(request):
	if request.user.is_authenticated():
		try:
			teacher = TeacherProfile.objects.get(teacher_id=request.session.__getitem__('uname'))
			booklist = Book.objects.filter(added_by=teacher).order_by('-create_date')

			return render(request, "books.html", {"booklist":booklist},)
		except TeacherProfile.DoesNotExist:
			return render(request, "books.html", {"error_msg":_("There is no such teacher!")},)
	else:
		return HttpResponseRedirect("/")
		
	
def addbook(request):
	if request.user.is_authenticated():
		try:
			teacher = TeacherProfile.objects.get(teacher_id=request.session.__getitem__('uname'))
			booklist = Book.objects.filter(added_by=teacher).order_by('-create_date')[:10]
			allowedbranches = Branch.objects.get(Q(name__iendswith = "language") & Q(id = request.session.__getitem__('branch')))
	#		query = allowedbranches.query

			book = Book(language=allowedbranches.id, branch = allowedbranches, added_by = teacher)			
			if request.method == "POST":
				#return render(request, "courses.html", {"post":request.POST, "file": request.FILES})		
				bookform = BookForm( request.POST, request.FILES, instance = book)

				if 	bookform.is_valid():
					if request.FILES.has_key('bookimage'):
						uploadedfile = request.FILES['bookimage']
						twohundredkilobytes = 200*1024
						if uploadedfile.size > twohundredkilobytes:
							return render(request, "addbook.html", {"form": bookform, "error_msg":_("Image is too big") ,"booklist":booklist })

					bookform.save()
					bookform=BookForm()
					return render(request, "addbook.html", {"form": bookform, "booklist":booklist},)
				else:
					return render(request, "addbook.html", {"form": bookform, "booklist":booklist}) 				
				
			else:
				bookform = BookForm()	
			return render(request, "addbook.html", {"form": bookform, "booklist":booklist},)

		except Branch.DoesNotExist:
			return render(request, "addbook.html", {"error_msg":_("Your branch not allowed!")},)

		except KeyError,TeacherProfile.DoesNotExist:
			bookform = BookForm()	
			return render(request, "addbook.html", {"form": bookform, "error_msg":_("There is no such teacher!")},)
	else:
		return HttpResponseRedirect("/")

def bookcontent( request, bookid ):
	try:
		book = Book.objects.get(id = bookid )
	except Book.DoesNotExist:
		pass
	return render(request, "bookcontent.html", {"book":book})


##############create course view all ####################

#VIEW ALL COURSE BOOKS
def allcoursebooks(request, grade):

	if request.user.is_authenticated():
		gradeview = getclassview(grade)
		try:
			course = Course.objects.get( teacher_id = request.session.__getitem__('uname'), grade = grade )
			cbooks = CourseBook.objects.filter( course = course ).order_by("-id")
		except Course.DoesNotExist:	
			cbooks = None
	return render(request, "coursebooks.html", {"cbooks":cbooks, "index": grade})

#CALLED ON FIRSTLY REDIRECT TO SMALLEST GRADE
def createcourse(request):
	classview = GRADE_CHOICES[0][0]
	return HttpResponseRedirect("/course/"+str(classview)+"/")	
#	return HttpResponseRedirect("/welcome/")


def editcoursegrade(request, grade):

	if request.user.is_authenticated():
		gradeview = getclassview(grade)
		try:
			course = Course.objects.get( teacher_id = request.session.__getitem__('uname'), grade = grade )
			cbooks = CourseBook.objects.filter( course = course ).order_by("-id")
		except Course.DoesNotExist:	
			cbooks = None

		msg_error=""
		if request.method == "POST":
			searchform = SearchForm(request.POST)

			if searchform.is_valid():
				search = searchform.cleaned_data['search']
				if len(search)  > 0:

					searchresult = searchbook(search, cbooks)

					return render(request, "editcourse.html", {"index": grade, "grade":gradeview, "searchform":searchform,
			"books": searchresult, "cbooks":cbooks, "search": search })

		else:	
			searchform = SearchForm()

		return render(request, "editcourse.html", {"index": grade, "grade":gradeview, "searchform":searchform, "msg_error":msg_error, "cbooks":cbooks })
	else:
		return HttpResponseRedirect("/")

def addcoursebook(request, grade, bookid, search):
	#return HttpResponse(search)

	if request.user.is_authenticated():

		searchform = SearchForm()
		if request.method == "GET":	
			try:
				ii = GRADE_CHOICES[int(grade)-1][0]
				classview = GRADE_CHOICES[int(grade)-1][1]
				teacher_obj = TeacherProfile.objects.get(teacher_id=request.session.__getitem__('uname'))
			
				course = Course.objects.get(grade=ii, teacher=teacher_obj)
				book = Book.objects.get(id=bookid)
				cbook = CourseBook()
				cbook.course = course
				cbook.book = book
				cbook.save()
			except IndexError,TeacherProfile.DoesNotExist: 
				return render(request, "editcourse.html", {"index": grade, "grade":classview, "searchform":searchform, "error_msg": "Index error"}) 
			
			except Course.DoesNotExist:

				course = Course()
				course.grade = ii
				course.teacher = teacher_obj
				course.name = classview+" %s"%"kurs"
				course.save()	

				book = Book.objects.get(id=bookid)
				cbook = CourseBook()
				cbook.course = course
				cbook.book = book
				cbook.save()

	 		except Book.DoesNotExist,err:
				return render(request, "editcourse.html", {"index": grade, "grade":classview, "searchform":searchform, "error_msg": err}) 

#		return HttpResponseRedirect("/course/"+str(ii)+"/p/")	
		return HttpResponseRedirect("/course/"+str(ii)+"/"+search+"/")	
	else:
		return HttpResponseRedirect("/")


#CALLED AFTER "addcoursebook" WHEN NEW BOOK ADDED TO COURSE AND RETURN LIST OF BOOKS THAN MATCHES SEARCH STRING
def afterbookadded(request, grade, search):

	try:
		course = Course.objects.get( teacher_id = request.session.__getitem__('uname'), grade = grade )
		cbooks = CourseBook.objects.filter( course = course ).order_by("-id")
	except Course.DoesNotExist:	
		cbooks = None

	searchresult = searchbook(search, cbooks)

	data={"search": search}
	searchform = SearchForm(data)

	gradeview = getclassview(grade)

	return render(request, "editcourse.html", {"index": grade, "grade":gradeview, "searchform":searchform, "msg_error":"", "cbooks":cbooks,"books": searchresult, "search": search })

"""
SIMPLE METHODS
"""
def deletefromlist(request, gradeindex, bookid):

	if request.method == "GET":
		try:
			course = Course.objects.get( teacher_id = request.session.__getitem__('uname'), grade = gradeindex )
			cbooks = CourseBook.objects.filter( course = course, book = bookid )
			cbooks.delete()
		except Course.DoesNotExist:	
			pass
	return HttpResponseRedirect("/course/"+gradeindex)	


"""
SIMPLE METHOD MAKE SEARCH BY
"""
def searchbook(search, cbooks):

	searchresult = []
	books = Book.objects.filter(Q(isbn__contains = search)|Q(name__icontains=search))

	for book in books:
		subresult = {}
		arraysize=len(searchresult)
		subresult["id"]	= book.id 
		subresult["name"] = book.name 
		subresult["isbn"] = book.isbn 
		subresult["added"] = 0 
		searchresult.append(subresult)	

		if cbooks is not None:
			for cbook in cbooks:
				if book.id == cbook.book_id:
					searchresult[arraysize]["added"] = 1

	return searchresult


#SIMPLE METHOD RETURN GRADE VIEW(7,9,8,10)
def getclassview(grade):
	#Here we redirect to seventh grade 	
	try:
		classview = GRADE_CHOICES[int(grade)-1][1]
	except IndexError:	
		classview = GRADE_CHOICES[0][0]
		return HttpResponseRedirect("/course/"+str(classview))	
	#Here we redirect to seventh grade 	
	return classview


##############create course view all end####################

	
def fillresults(request):
	classview = GRADE_CHOICES[0][0]
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse("studentslist", args={str(classview)}))
	else:
		return HttpResponseRedirect("/")
		
def studentslist(request, gradeindex):

	if request.user.is_authenticated():
		#list of students and list of books for this grade and teacher	
		classview = GRADE_CHOICES[int(gradeindex)-1][1]

		schoolid = TeacherProfile.objects.get( teacher_id = request.session.__getitem__('uname') ) 
		#get students with school id and grade 
		students = StudentProfile.objects.filter( school_id = schoolid.school_id , class_field = classview).order_by("kz_surname")
		#trying to get course for grade
		try:
			course = Course.objects.get( teacher_id = request.session.__getitem__('uname'), grade = gradeindex )
		except Course.DoesNotExist:
			return render(request, "results_msg.html",{"error_msg":_("There is no course for grade"), "classview":classview, "grade":gradeindex })
		
		#get all books related to this course
		cbooks = CourseBook.objects.filter( course = course )
		query  = cbooks.query
		
		#get last ten readmore objects for right panel
		recentactivity = ReadMore.objects.filter(course = course ).order_by("-id")[:10]
		#get last ten readmore objects
		readmorelist = ReadMore.objects.filter(course = course ).order_by("-id")

		#adds all red book to specified student id
		#first if there exist such key then simply adds book id
		#else if not then create new arraw for this student id
		readmoredict={}
		for readmore in readmorelist:
			try:
				readmoredict[readmore.student.student_id].append(readmore.book.id)		
			except KeyError:
				readmoredict[readmore.student.student_id] = []
				readmoredict[readmore.student.student_id].append(readmore.book.id)		
				pass
		

		studentlist = []	
		for student in students:
			try:
				#select all books except that books which are already red
				booksredbystudent = readmoredict[student.student_id]
				ostatok_knig = CourseBook.objects.filter(course = course).exclude(book__in=booksredbystudent)
				query  = cbooks.query

				studentlist.append({"studentid":student.student_id, "bookred":[1,2], "listcontent":ostatok_knig, "student":student})  

			except KeyError:		
				studentlist.append({"studentid":student.student_id, "bookred":None,"listcontent":None, "student":student})  
				pass
	
		return render( request, "results.html",
			{
			 "students": students, 
			 "cbooks":cbooks, 
			 "courseid": course.id, 
			 "gradeid":gradeindex, 
			 "readmorelist":readmorelist, 
			 "studentlist":studentlist,
			 "readmoredict":readmoredict,
			 "query":query, 
			 "recentactivity":recentactivity
			}) 

	else:
		return HttpResponseRedirect("/")

	
def savebookred(request):

	if request.user.is_authenticated():
#		branches = {5:"english",9:"kazakh",10:"turkish",11:"russian"}	
		if request.method == "POST":

			studentid = request.POST["studentid"]
			bookred =   request.POST["bookred"]
			courseid =  request.POST["courseid"]
			gradeid =   request.POST["gradeid"]

			teacher = TeacherProfile.objects.get( teacher_id = request.session.__getitem__('uname') ) 
			student = StudentProfile.objects.get( student_id = studentid ) 
			course =  Course.objects.get( id= courseid) 
			try:
				book =    Book.objects.get( id= bookred) 
				readmore = ReadMore()
				readmore.book=book
				readmore.course=course
				readmore.student=student
				readmore.added_by=teacher
				readmore.save()

			except Book.DoesNotExist:
				pass					

		return HttpResponseRedirect("/results/"+gradeid)
	else:
		return HttpResponseRedirect("/")

"""
#s	return HttpResponse(schoolid.school_numeric_id)	

			if readmoredict[int(readmore.student.student_id)] is not None:
				readmoredict[int(readmore.student.student_id)].append(readmore.book.id)
			else:
				readmoredict[int(readmore.student.student_id)] = []
				readmoredict[int(readmore.student.student_id)].append(readmore.book.id)

"""
