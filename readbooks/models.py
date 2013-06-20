from django.db import models
import datetime
from django.utils.translation import ugettext_lazy as _

BOOK_FORMAT = (
(1, 'A4'),
(2, 'A5'),
)

CHOICES = (
(1, 'Kazakh Language'),
(2, 'Russian Language'),
(3, 'English Language'),
(4, 'Turkish Language'),
)

GRADE_CHOICES = (
(1, '7'),
(2, '8'),
(3, '9'),
(4, '10'),
(5, '11'),
)

class Book(models.Model):

	language = models.IntegerField()
	branch = models.ForeignKey("Branch")
	added_by = models.ForeignKey("TeacherProfile", to_field='teacher_numeric_id')

	name = models.CharField(max_length=255, verbose_name=_("Name"))
	isbn = models.CharField(max_length=13, unique = True, verbose_name=_("ISBN"))
	pages = models.IntegerField(verbose_name=_("Pages"))
	format = models.IntegerField(choices=BOOK_FORMAT, verbose_name=_("Format"))
	bookimage = models.ImageField(upload_to = "uploads/", default="uploads/default.png", verbose_name=_("BookImage"))
	create_date = models.DateTimeField(default= datetime.datetime.now())

	def __unicode__(self):
		return self.name

class Course(models.Model):

	grade = models.IntegerField(choices=GRADE_CHOICES)
	teacher =models.ForeignKey("TeacherProfile", to_field ="teacher_numeric_id")
	name = models.CharField(max_length=255)
	create_date = models.DateTimeField(default=datetime.datetime.now())

	def __unicode__(self):
		return self.name

class CourseBook(models.Model):

	course = models.ForeignKey("Course")
	book = models.ForeignKey("Book")

class ReadMore(models.Model):

	book = models.ForeignKey("Book")
	course = models.ForeignKey("Course")	
	student = models.ForeignKey("StudentProfile")
	added_by = models.ForeignKey("TeacherProfile", to_field = "teacher_numeric_id")
	create_date = models.DateTimeField(default=datetime.datetime.now())	
	
class StudentProfile(models.Model):

    student_id = models.IntegerField(unique=True)
    school_id = models.CharField(max_length=15)
    school_numeric_id = models.IntegerField()
    kz_name = models.CharField(max_length=60)
    kz_surname = models.CharField(max_length=90)
    class_field = models.IntegerField(db_column='class') # Field renamed because it was a Python reserved word.
    division = models.CharField(max_length=9)
    password = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=30)
    edit_time = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
		return self.kz_name

    class Meta:
        db_table = u'katev_production_students_info'

class TeacherProfile(models.Model):

    teacher_id = models.CharField(max_length=5, unique=True)
    teacher_numeric_id = models.IntegerField(unique=True)
    school_id = models.CharField(max_length=18)
    school_numeric_id = models.IntegerField()
    kz_name = models.CharField(max_length=60)
    kz_surname = models.CharField(max_length=150)
    gorev_short = models.CharField(max_length=45)
    branch_id = models.IntegerField(null=True, blank=True)
    pas = models.CharField(max_length=60)
    edit_time = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
		return self.teacher_id

    class Meta:
        db_table = u'katev_production_teacher_info'


class KtlSchools(models.Model):
    kz_description = models.CharField(max_length=600, blank=True)
    en_description = models.CharField(max_length=600, blank=True)
    sch = models.CharField(max_length=9, blank=True)
    sch_numeric_id = models.IntegerField()
    ru_description = models.CharField(max_length=600, blank=True)
    tr_description = models.CharField(max_length=600, blank=True)
    tr_description_short = models.CharField(max_length=75)
    status = models.CharField(max_length=60, blank=True)
    class Meta:
        db_table = u'ktl_schools'
	
class Branch(models.Model):

    name = models.CharField(max_length=135, blank=True)
    general_name = models.CharField(max_length=135, blank=True)
    kz_general_name = models.CharField(max_length=135)
    tr_general_name = models.CharField(max_length=135)
    ru_general_name = models.CharField(max_length=135)
    short_name = models.CharField(max_length=60, blank=True)
    tr_short_name = models.CharField(max_length=18)
    class Meta:
        db_table = u'sb_teacher_branch'



class KatevProductionStudentsInfo(models.Model):

    student_id = models.IntegerField(unique=True)
    school_id = models.CharField(max_length=15)
    kz_name = models.CharField(max_length=60)
    kz_surname = models.CharField(max_length=90)
    en_name = models.CharField(max_length=60)
    en_surname = models.CharField(max_length=90)
    class_field = models.IntegerField(db_column='class') # Field renamed because it was a Python reserved word.
    lang_group = models.CharField(max_length=9)
    division = models.CharField(max_length=9)
    password = models.CharField(max_length=30, blank=True)
    nationality = models.CharField(max_length=60, blank=True)
    birth = models.DateField(null=True, blank=True)
    father = models.CharField(max_length=300, blank=True)
    mother = models.CharField(max_length=300, blank=True)
    gender = models.CharField(max_length=30)
    edit_time = models.DateTimeField()
    class Meta:
        db_table = u'katev_production_students_info'

class KatevProductionTeacherInfo(models.Model):

    tt_id = models.CharField(max_length=30, primary_key=True)
    teacher_id = models.CharField(max_length=18, primary_key=True)
    teacher_numeric_id = models.IntegerField()
    school_id = models.CharField(max_length=18)
    school_numeric_id = models.IntegerField()
    kz_name = models.CharField(max_length=60)
    kz_surname = models.CharField(max_length=150)
    kz_middle_name = models.CharField(max_length=60, blank=True)
    en_name = models.CharField(max_length=60)
    en_surname = models.CharField(max_length=150)
    en_middle_name = models.CharField(max_length=60, blank=True)
    gorev = models.CharField(max_length=120, blank=True)
    gorev_short = models.CharField(max_length=45)
    branch_id = models.IntegerField(null=True, blank=True)
    branch = models.CharField(max_length=150, blank=True)
    university = models.CharField(max_length=210, blank=True)
    pas = models.CharField(max_length=60)
    edit_time = models.DateTimeField()
    birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=15, blank=True)
    nationality = models.CharField(max_length=60, blank=True)
    lesson_time = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'katev_production_teacher_info'
	
#	username	password	userid	userlevel	email	timestamp	parent_directory

class OldUsers(models.Model):
#	id = models.IntegerField(default=None)
	username = models.CharField(max_length = 100, primary_key=True)
	password = models.CharField(max_length = 100)	 
#	user_id = models.CharField(max_length = 200)	 
	userlevel = models.IntegerField()
	email = models.EmailField()
	class Meta:
		db_table=u'users'



