from django.db import models
from quiz_generator.models import SbQuestions
from readbooks.models import TeacherProfile
import datetime


class SbQuestionRating(models.Model):
	#One to One
	#one row for each question, stores rate amount and value
    question = models.ForeignKey(SbQuestions)
    rate_amount = models.IntegerField(default=0)
    rate_value = models.IntegerField(default=0)
    max_rate = models.IntegerField(default=5)

    class Meta:
        db_table = u'sb_question_rating'

	def __unicode__(self):
		return self.rate_amount	

class SbRatedBy(models.Model):
	#Many to One
	#can store mulpiple rows for one question, stores user id and comment 
	question = models.ForeignKey(SbQuestions)
	user_id	= models.IntegerField()
	comment = models.CharField(max_length = 255L)

	class Meta:
		db_table = u'sb_rated_by'

	def __unicode__(self):
		return str(self.user_id)+"  "+ str(self.comment)	


class NotificationTypes(models.Model):
	name = models.IntegerField()
	text_tr = models.CharField(max_length=40)
	text_kz = models.CharField(max_length=40)

class Notifications(models.Model):

	question= models.IntegerField()
	notification = models.ForeignKey(NotificationTypes)
	date_filled=models.DateTimeField(default = datetime.datetime.now())

class BadQuestionStats(models.Model):
	
	amount = models.IntegerField()
#	deleted_amount = models.IntegerField()
	date_filled = models.DateTimeField(default = datetime.datetime.now())

		
