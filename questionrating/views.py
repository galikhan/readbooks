# Create your views here.
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from models import SbQuestionRating, SbRatedBy, NotificationTypes, Notifications
from quiz_generator.models import SbQuestions
from readbooks.models import TeacherProfile
import datetime,simplejson

def two_week_old_questions(request):

	#Number of teachers that made rating for this question[cant be zero]
	rated_people = 1
	#Average amount of rating for this question [1-5]
	rate_min = 6

	#First step notify users for 2 week left to delete bad questions
#	timedelta = 1	
#	trash = perform_calculation(timedelta, rated_people, rate_min)

	#First step notify users for 1 week left to delete bad questions
#	timedelta = 7
#	trash = perform_calculation(timedelta, rated_people, rate_min)


	#First step notify users for today will delete bad questions
	timedelta = 14	
	trash = perform_calculation(timedelta, rated_people, rate_min)
	amount = trash.__len__()
#	BadQuestionStats.objects.create(amount = amount).save()	
	delete = SbQuestions.objects.using("katev").filter(id__in=trash).delete()

	return render(request, "qr-index.html", {"trash": trash, "delete":delete },)
			
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


def save_question_rating(request):

	if request.is_ajax():
		#user = request.session.__getitem__('username')
		#user = request.session.user
		user = 11111
		question_id = request.POST["q-id"]
		rate_value = request.POST["rate"]
		comment = request.POST["comment"]
		with_comment = request.POST["type"]

		question_obj = SbQuestions.objects.using('katev').get( id = question_id )

		rating,crated = SbQuestionRating.objects.using('katev').get_or_create( question = question_obj )
		rating.rate_amount = int(rating.rate_amount) + int(1)
		rating.rate_value = int(rating.rate_value) + int(rate_value)
		rating.save()		

		rated_by,created = SbRatedBy.objects.using('katev').get_or_create( question = question_obj, user_id = user )
		rated_by.comment = comment
		rated_by.save()

		amount = rating.rate_amount
		value = rating.rate_value

		if value == 0:
			value = 1
		rating_value = round(float(value)/amount,2)

		json = simplejson.dumps({'insert':True, 'comment_whole':comment, 'rating':rating_value })
		return HttpResponse( json, "application/json" )

	return HttpResponse("save q")

