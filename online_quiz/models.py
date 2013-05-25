from django.db import models
from quiz_generator.models import QuizList, QuestionCart
import datetime

class QuizTracker(models.Model):

	quiz = models.ForeignKey(QuizList)
	user = models.IntegerField()
	active_question = models.IntegerField()
	result = models.IntegerField( default=0 )
	start_date = models.DateTimeField( default = datetime.datetime.now() )
	end_date = models.DateTimeField( null = True )	

class QuizAnswers(models.Model):

	quiz_tracker = models.ForeignKey(QuizTracker)
	question_cart = models.IntegerField()#this mean question id 
	answer = models.IntegerField( default = 0 )#this mean variant id
	order = models.IntegerField( default = 0 )# store the order of question




	



