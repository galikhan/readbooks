from models import SbTopicsList, SbSubtopicsList, SbQuestions, SbClass, QuizList, QuestionCart
from django.shortcuts import render
from django.http import HttpResponse, Http404
from questionrating.models import SbQuestionRating, SbRatedBy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
import simplejson, datetime

def typeahead(request):
	array = ['gali', 'gattuso', 'gattaka']
	json = simplejson.dumps(array)
	return  HttpResponse( json, "application/json" )

def topics_with_subtopics(user_branch):

	grade_class = SbClass.objects.using('katev').all().order_by("number_view")
	for grade in grade_class:

		topics = grade.sbtopicslist_set.filter(class_field = grade.id, branch = user_branch).order_by("class_field__number_view", "quarter")
#		for t in topics:
#			subtopics = t.sbsubtopicslist_set.filter(topic=t.id)
#			question_num = 0
#			for subtopic in subtopics:
#				question_num += subtopic.number_of_questions

#			t.subtopics = subtopics
#			t.total_questions_amount = question_num

		grade.topics = topics

	# lets count questions with common topics 
	# insrt them into associative array then extract while loop of topics array
	return grade_class

def list_questions_by_page( request, topic_id, subtopic_id, index ):

	user = request.session.__getitem__("uname")
	user_branch = request.session.__getitem__("branch")

	tws = topics_with_subtopics( user_branch )
	questions = gather_questions( topic_id, subtopic_id, user )

	page, pages = paginate( index, questions )		
	quiz_id, question_num = check_quiz( user )

	return render(request, "quiz.html",  
		{ "tws":tws, 
		"questions":page, 
		"pages" : pages, 
		"index": int(index), 
		"topic_id":topic_id, 
		"subtopic_id" : subtopic_id, 
		"quiz_id":quiz_id,
		"question_num":question_num,
		})

def list_questions( request, topic_id, subtopic_id ):

	user = request.session.__getitem__("uname")
	user_branch = request.session.__getitem__("branch")
	
	tws = topics_with_subtopics( user_branch )
	questions = gather_questions( topic_id, subtopic_id, user )
	index = 1
	page, pages = paginate( index, questions )		
	quiz_id, question_num = check_quiz( user )

	return render(request, "quiz.html",  
		{ "tws":tws, 
		"questions":page, 
		"pages" : pages, 
		"index": int(index), 
		"topic_id":topic_id, 
		"subtopic_id" : subtopic_id,
		"quiz_id":quiz_id,
		"question_num":question_num,
		})

def list_topics(request):

	user = request.session.__getitem__("uname")
	user_branch = request.session.__getitem__("branch")

	tws = topics_with_subtopics( user_branch )
	quiz_id, question_num = check_quiz( user )
#	tws = []
	return render(request, "quiz.html",  
		{ "tws":tws, 
		"quiz_id":quiz_id,
		"question_num":question_num,
		})

def create_new_quiz(request):

	if request.is_ajax():
		user = request.session.__getitem__("uname")

		#must delete all bindings
		QuizList.objects.get(id = request.POST['current-quiz-id']).delete()

		quizlist = QuizList()
		quizlist.user = user
		quizlist.number_of_questions = 0
		quizlist.save()

		id = quizlist.id

		json = simplejson.dumps({"quiz_id" : id , "question_num" :0 })
		return HttpResponse( json, "application/json" )
	else :
		return Http404()	


def check_quiz( user_id ):

	try:
		quiz = QuizList.objects.get( user = int(user_id), create_date = None )
		quiz_id = quiz.id
		question_num = quiz.number_of_questions
		return quiz_id, question_num

	except QuizList.DoesNotExist:
		pass
		return 0, 0

def generate_quiz( request ):

	if request.is_ajax():

		quiz_id = request.POST["quiz-id"]
		type = request.POST["type"]
		args = request.POST["args"]
		name = request.POST["name"]

		try:
			quiz = QuizList.objects.get(id = quiz_id)
			quiz.create_date = datetime.datetime.now()
			quiz.name = name
			quiz.save()
		except QuizList.DoesNotExist:
			pass	

#		if type == "paper-quiz":
			#call method from paper quizm model
#		elif type == "mve-quiz":
			#
#		else:
			#
		#Obnulyaem quiz id and question num 	
		json = simplejson.dumps({"quiz_id" : 0 , "question_num" :0 })
		return HttpResponse(json, "application/json")
	else:
		return Http404	

def gather_questions( topic_id, subtopic_id, user ):

	# set by 20 questions on each page for now will be 1
	questions = SbQuestions.objects.using('katev').filter( d_subtopic_id = subtopic_id )

	for question in questions:
		qtype = question.d_q_type.short_name
		try:
			rate_object = SbQuestionRating.objects.using('katev').get( question = question ) 	
			question.rating = round(float(rate_object.rate_value) / rate_object.rate_amount, 2)
		except SbQuestionRating.DoesNotExist:	
			question.rating = 0.0
			pass

		try:
			user_comments = SbRatedBy.objects.using('katev').filter( question = question ).order_by("-id")[:3]
			user_ratings = SbRatedBy.objects.using('katev').get( question = question, user_id = user )
			question.allow_rating=False
		except:
			question.allow_rating=True
			pass
		question.user_comments = user_comments

		if qtype == 'single_answer' or qtype == 'multiple_answer' or qtype == 'true_false':
			question.meta = 'variants'
			question.variants = question.sbvariants_set.all().order_by("id")
			question.variant_answers = question.sbanswers_set.all().order_by("view_order")

		elif qtype == 'mappings':
			question.meta = 'mappings'
			question.mappings = question.sbquestionmappings_set.all().order_by("id")
		else:
			question.meta = 'other'

	return questions		

def paginate(index, questions):

	paginator = Paginator( questions, 5 )
	try:
		page = paginator.page(index) 
	except PageNotAnInteger:
		index = 1
		page = paginator.page(index) 
	except EmptyPage:
		index = paginator.page_range
		page = paginator.page(index) 
	pages = paginator.page_range

	return page, pages

def add_remove_questions_to_cart( request ):

	if request.is_ajax():
		#create quiz with current user id and add question
		#also must send message which will tell to create new or complete previous quiz for this topic
		user = request.session.__getitem__('uname')
		quiz_id = request.POST['quiz-id']
		question_id = request.POST['question-id']

		if quiz_id == "0":

			quiz = QuizList.objects.create( user = user, number_of_questions = 1 )
			question = quiz.questioncart_set.create( question = question_id )
			id = quiz.id

			json = simplejson.dumps({"quiz_id" : id , "question_num" :1})
			return HttpResponse( json, "application/json" )

		else:
			try:	
				quiz = QuizList.objects.get( pk = quiz_id )
				question = quiz.questioncart_set.create( question = question_id )
				quiz.number_of_questions += 1
				quiz.save()

				json = simplejson.dumps({ "quiz_id" : quiz.id, "question_num" : str(quiz.number_of_questions) })

			except QuizList.DoesNotExist:
				json = simplejson.dumps("DoesNotExist")
				pass

			return HttpResponse( json, "application/json" )

	else:
		return HttpResponse("Not an ajax call")

def count_questions(request):
	#Must be called once to kknow number of questions for each subtopic
	#temporary function then must be changed with automatic increase of value in number_of_field field
	#now it only updates values of current topics..count()
	topics = SbTopicsList.objects.using('katev').all()

	subtopics = SbSubtopicsList.objects.using('katev').filter( topic__in = topics )
	for sub in subtopics:
		questions_count = SbQuestions.objects.using( 'katev' ).filter( d_subtopic_id = sub.id ).count()
		sub.number_of_questions = questions_count
		sub.save()
		#print sub.name , questions


				
