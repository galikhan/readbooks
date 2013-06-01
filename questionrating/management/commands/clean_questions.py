import os, sys
sys.path.append('/home/katevkz/public_html/readbooks')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "readbooks.settings")

from django.core.management.base import BaseCommand,CommandError
from questionrating.models import *
import datetime

class Command(BaseCommand):
	def handle(self, *args, **options):
		
		#Number of teachers that made rating for this question[cant be zero]
		rated_people = 3
		#Average amount of rating for this question [1-5]
		rate_min = 2.5

		#First step notify users for 2 week left to delete bad questions
		#	timedelta = 1	
		#	trash = perform_calculation(timedelta, rated_people, rate_min)

		#First step notify users for 1 week left to delete bad questions
		#	timedelta = 7
		#	trash = perform_calculation(timedelta, rated_people, rate_min)


		#First step notify users for today will delete bad questions
		#1 day
		timedelta = 1	
		trash = perform_calculation(timedelta, rated_people, rate_min)
		
		all = SbQuestions.objects.using('katev').all()
		count_all = all.count() 
		
		amount = trash.__len__()

		BadQuestionStats.objects.create(amount = count_all, deleted_amount = amount ).save()	
#		delete = SbQuestions.objects.using("katev").filter(id__in=trash).delete()	

#	return render(request, "qr-index.html", {"trash": trash, "delete":delete },)
			
#	return render(request, "qr-index.html", {"questions":qafter,"qafterq":qafter.query, "query": q.query, "trash": trash})

def perform_calculation(timedelta, rated_people, rate_min):

	if timedelta >= 0:
		q = SbQuestions.objects.using("katev").filter(date_filled__lt=(datetime.datetime.now()-datetime.timedelta(days=timedelta))).values("id","teacher_id","date_filled","sbquestionrating__rate_amount","sbquestionrating__rate_value")
	
		trash = []
		for question in q:
			value  = question["sbquestionrating__rate_value"]
			amount = question["sbquestionrating__rate_amount"]

			if amount >= rated_people:
				avg = value/amount
				if avg <= rate_min:
					trash.append(question["id"])		
#					trash.append(str(question["id"])+" -- "+str(question["date_filled"]))		
#		qafter = SbQuestions.objects.using("katev").filter(id__in=trash)
		return trash

	else:
		return "Incorrect timedelta"+str(timedelta)
