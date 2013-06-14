from django.db import models
import datetime

class EnglishCertificates(models.Model):
	student = models.IntegerField()
	level = models.ForeignKey("EnglishLevel")

class TurkishCertificates(models.Model):
	student = models.IntegerField()
	level = models.ForeignKey("TurkishLevel")

class TurkishLevel(models.Model):
	name = models.CharField(max_length=10)	

class EnglishLevel(models.Model):
	name = models.CharField(max_length=20)	

class CertificateLinks(models.Model): 

    school = models.IntegerField()
    certificate_type = models.CharField( max_length = 10 )
    name = models.CharField( max_length = 100 )
    date_created = models.DateTimeField(default=datetime.datetime.now())

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
        ordering = ["en_name"]

