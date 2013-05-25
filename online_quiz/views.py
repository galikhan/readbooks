from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from quiz_generator.models import SbQuestions, SbVariants, SbAnswers, SbQuestionType, QuizList, QuestionCart, SbClass
from models import QuizTracker, QuizAnswers
from django.core.urlresolvers import reverse
import simplejson, datetime, random
from django.core import serializers
from django.utils.datastructures import SortedDict

# 1 predefined list of questions
def load_question( quiz_id, current_question, max_number_of_questions ):

	minus_one = current_question - 1

	if current_question <= max_number_of_questions :
		#this mean that quiz questions are over	
		#print current_question,' plus 1 = > ',current_question_plus1
		questions = QuestionCart.objects.filter( quiz_list = quiz_id ).order_by("id")[minus_one:current_question]
#		questions = QuestionCart.objects.filter( quiz_list = quiz_id ).order_by("id")[0:1]
		for question in questions:
			try:
				question_real = SbQuestions.objects.using('katev').get( id = question.question )
				variants = question_real.sbvariants_set.all()
			except SbQuestions.DoesNotExist:	
				question_real = None
				variants = []
				pass
	else:	
		question_real = None
		variants = []
	return question_real, variants

#show list of predefined quizzes
def online_quiz( request ):

	quiz_list = QuizList.objects.all()
	return render( request, "online-quiz.html", {"list": quiz_list} )

#save user answer
def save_answer( variant_ids, question_id, tracker_object, order ):

	if len(variant_ids) == 0: 
		QuizAnswers.objects.create( quiz_tracker = tracker_object, question_cart = question_id, answer = 0 ,order = order )				
	else:	
		delete_previous = tracker_object.quizanswers_set.filter( question_cart = question_id, order = order ).delete()
		for vid in variant_ids:
			obj = QuizAnswers.objects.create( quiz_tracker = tracker_object, question_cart = question_id, answer = vid ,order = order )	

#main method that accepts user answers and send next or prev questions
def run_online( request, quiz_id, tracker_id ):

	quiz = QuizList.objects.get( id = quiz_id )
	user = request.session.__getitem__("uname")
	try:
		tracker = QuizTracker.objects.get( quiz = quiz, user = user, end_date = None )
	except QuizTracker.DoesNotExist:
		return HttpResponseRedirect( reverse( "online_quiz" ))

	question_number = quiz.number_of_questions

	if request.is_ajax():
		# if ajax we can call next , skip , previous
		stream_state = True
		step = request.POST["step"]
		answer = simplejson.loads(request.POST["answer"])	
		#shows current question number (1,2,3,4...) not id of question
		current_question = int(request.POST["order"])
		question_id = request.POST["question-id"]

		current_question, disable_button = cur_question_and_dis_button( step, current_question, question_number, answer,  question_id, tracker )
		order = current_question
		if disable_button == "outofbound":
			# esli out of bound to zakanchivaem exam i otpravlyaem result_count
			quiz_result_info = result_count( user, quiz_id, tracker_id )
			quiz_result_info["disable_button"] = "outofbound"
			json = simplejson.dumps(quiz_result_info)
			return HttpResponse(json, "application/json")
		else:	
			question_real, variants = load_question( quiz_id, current_question, question_number )
			tracker.active_question = current_question
			tracker.save()

		if question_real is not None:
			question = question_real.question
			id = question_real.id
			mod_variants = set_user_checks( tracker, variants, order )
		else:
			question = None	
			id = None


		json = simplejson.dumps({ 
				"total_qnum":question_number,
				"disable_button":disable_button,
				"stream_state":stream_state,
				"variants": [str(variant.name) for variant in variants], 
				"variant_ids": [str(variant.id) for variant in variants], 
				"checked_variants" : [str(variant) for variant in mod_variants], 
				"question": question , 
				"id": id,  
				"current_question":current_question, 
				"quiz_id":quiz_id,
			    "tracker_id":tracker_id })		

		return HttpResponse( json, "application/json" )	
		# Must get one question with variants if exist
	else:
		# if else then it is first question or simple page update	
		# do not increment current_question
		current_question = tracker.active_question
		order = current_question
		# Must get one question with variants if exist
		question_real, variants = load_question( quiz_id, current_question,  question_number )

		if question_real is not None:
			question = question_real.question
			id = question_real.id
			mod_variants = set_user_checks( tracker, variants, order )
			for variant, mod in zip(variants, mod_variants):
				variant.checked = mod
		else:
			question = None	
			id = None


	return render( request, "online-quiz.html", 
		{
		"total_qnum":question_number,
		"question" :question,
		"id": id,
		"quiz_id" : quiz_id,
		"tracker_id" : tracker.id,
		"current_question" : tracker.active_question ,
		"variants":variants,
		"checked_variants": mod_variants, 
		"start_date" : tracker.start_date,
		})	


def set_user_checks( tracker, variants, order ):
	#this method return new modified array with user checked answers
	quiz_answers = QuizAnswers.objects.filter( quiz_tracker = tracker, order=order ).order_by("id")
	mod_variants = []

	for index, v in enumerate(variants):
		mod_variants.append("")
		for a in quiz_answers: 
			if v.id == a.answer:
				mod_variants.insert(index, "checked")
				pass
	return 	mod_variants		
# count user result	
def result_count( user, quiz_id, tracker_id ):

#	user = request.session.__getitem__("uname")
	quiz = QuizList.objects.get( id = quiz_id )
	try:
		tracker = QuizTracker.objects.get( quiz = quiz, user = user, end_date = None )
	except QuizTracker.DoesNotExist:	
		return HttpResponseRedirect( reverse( "online_quiz" ))
	#Quiz Answers can store multiple answers for one question remember that!!!
	#can be multiple questions	
	quiz_answers = QuizAnswers.objects.filter( quiz_tracker = tracker ).order_by("id")
	number_of_questions = quiz.number_of_questions
	result = 0

	# PODSCHET RESULTATA #
	if number_of_questions == 0:
		number_of_questions = 1

	#round till 3rd element
	one_point = round( ( float( 100 ) / number_of_questions ) , 3 ) 
			
	question_ids = []
	questions_itself = {}
	for answer in quiz_answers:
		try:
			#na samom dele eto id voprosa a ne 'question cart'a
			qid = answer.question_cart

			question = SbQuestions.objects.using('katev').get( id = qid )	
			correct  = question.sbanswers_set.all()

			question_ids.append(qid)
			questions_itself[ question.id ] = question.question

			correct_num = correct.count()

			if correct_num == 0:
				correct_num = 1

			for ca in correct:
				if ca.variant_id == answer.answer:
					result += one_point / correct_num
		except SbQuestions.DoesNotExist:
			pass

	# SOHRANAYEM RESULTAT V TRACKER'E	
	tracker.result = result	
	tracker.end_date = datetime.datetime.now() 
	tracker.save()

	# ZAKANCHIVAYEM PODSCHET #	

	# Pokaz resultata
	number_of_questions = quiz.number_of_questions

	tracker = QuizTracker.objects.get( id = tracker.id )
	result = tracker.result

#	time_spent = "Start time : "+str( tracker.start_date.tzinfo() )+"<br>End time : "+str( tracker.end_date.tzinfo() )
	time_spent = str(tracker.end_date - tracker.start_date) 
#	print tracker.end_date,"-" ,tracker.start_date
#	print datetitime_spent

	quiz_result_info = { "number_of_questions":number_of_questions, "result" : result, "time_spent":time_spent, "start_date":str(tracker.start_date), "end_date": str(tracker.end_date) }
	return quiz_result_info
#	json = simplejson.dumps({ "disable_button" : "outofbound", "number_of_questions":number_of_questions, "result" : result, "time_spent":time_spent })
#	return HttpResponseRedirect( json, "application/json" ) 
#	return HttpResponseRedirect(reverse("result_show", kwargs = {
#		"quiz_id":quiz_id,
#		"tracker_id":tracker_id,
#		}))

# show user result	
	#set type = 5 for avoid conflict with previous types			

def result_show( request, quiz_id, tracker_id ):

	user = request.session.__getitem__("uname")
	quiz = QuizList.objects.get( id = quiz_id )
	try:
		tracker = QuizTracker.objects.get( id = tracker_id )
	except QuizTracker.DoesNotExist:	
		return Http404

	questions = QuestionCart.objects.filter( quiz_list = quiz ).order_by("id")

	question_ids = []
	questions_itself = {}

	for question in questions:
		qid = question.question
		question_ids.append(qid)
		try:
			question_itself = SbQuestions.objects.using('katev').get( id = qid )	
			questions_itself[question_itself.id] = question_itself.question 
		except	SbQuestions.DoesNotExist:
			pass

#	questions_itself = SortedDict(questions_itself)
# 	PODGOTOVKA DLYA OTOBROJENIYA DLYA USER #
	correct = SbAnswers.objects.using('katev').filter( question_id__in = question_ids )

	variants_array = {}
	variants = SbVariants.objects.using('katev').filter( question__id__in = question_ids ).order_by("question")
	user_answers = QuizAnswers.objects.filter( quiz_tracker = tracker ).order_by("order")
#	return HttpResponse(str(variants))	

	# three types ={1,2,3,4}={simple variant, incorrect variant, correct answer, user's correct answer}
	for u in user_answers:
		filter_variants = variants.filter( question__id = u.question_cart )	
		for v in filter_variants:
			variants_array[ str(v.question.id)+"_"+str(v.id)+"_"+str(u.order) ] = {"value":v.name,"type": 1 } 

#	return HttpResponse(str(variants_array))	
#	#setting type = 3 on correct variants	
	for u in user_answers:
		filter_correct = correct.filter( question__id = u.question_cart )	
		for c in filter_correct:
			variants_array[ str(c.question_id)+"_"+str(c.variant_id)+"_"+str(u.order) ]["type"] = 3

#	return HttpResponse(str(variants_array))	
	#setting type = 4 on correct, type = 2 on user incorrect variants

	user_answer_variants = {}
	ready_for_print_variants = {}
	for u in user_answers:
		try:
			vtype = variants_array[ str(u.question_cart)+"_"+str(u.answer)+"_"+str(u.order) ]["type"]
			value = variants_array[ str(u.question_cart)+"_"+str(u.answer)+"_"+str(u.order) ]["value"]
			#vtype +=1 
			variants_array[ str(u.question_cart)+"_"+str(u.answer)+"_"+str(u.order) ]["type"] += 1
			#if vtype == 3: #	vtype = 4#elif vtype == 1:	#	vtype = 2
		except KeyError:
			pass	

		filter_variants = variants.filter( question__id = u.question_cart )	
		for v in filter_variants:
			var_array = variants_array[ str(v.question.id)+"_"+str(v.id)+"_"+str(u.order) ]
			try:
				ready_for_print_variants[ str(u.question_cart)+"_"+str(u.order) ].append(var_array) 
			except KeyError:
				ready_for_print_variants[ str(u.question_cart)+"_"+str(u.order) ] = []
				ready_for_print_variants[ str(u.question_cart)+"_"+str(u.order) ].append(var_array) 
				pass

#	return HttpResponse(str(ready_for_print_variants))
	ready_for_print_results = []
	for index, qid in enumerate(question_ids):
		ready_for_print_results.append((index ,{"question": questions_itself[ qid ], "variants" : ready_for_print_variants[ str(qid)+"_"+str(index+1) ]}))
		

#	return HttpResponse(str(ready_for_print_results))
	ready_for_print_results	= SortedDict( ready_for_print_results )
	# ZAKANCHIVAYEM DLYA OTOBROJENIYA DLYA USER #
	return render(request, "online-quiz-result.html", { "ready_for_print_results":ready_for_print_results })		
	#json = simplejson.dumps(ready_for_print_results)
	#return HttpResponse( json, "application/json" )

# start online quiz create needed trackers 
def start_online( request, quiz_id ):

	# save it as active in Quiz Tracker but before check it for unfinished quiz table
	user = request.session.__getitem__("uname")
	quiz = QuizList.objects.get( id = quiz_id )

	try:
		tracker = QuizTracker.objects.get( quiz = quiz, user = user, end_date = None )
	except QuizTracker.DoesNotExist: 	
		tracker = QuizTracker.objects.create( quiz = quiz, user = user, active_question = 1 )
#		tracker.save()
		pass
	#in order to eliminate back call of this view redirect it
	tracker_id = tracker.id
	return HttpResponseRedirect(reverse("online_quiz.views.run_online", kwargs={ "quiz_id":quiz_id, "tracker_id":tracker_id } ))


# identify step and perform current_question
def cur_question_and_dis_button( step, current_question, question_number, answer,  question_id, tracker ):

	save_order = current_question
	if step == "next" or step == "skip":
		current_question = current_question + 1
	elif step == "previous":
		current_question = current_question - 1

	# 1,2 edges of question list ["first", "last"] questions
	# 3 middle of question list [first > "middle" <last] questions
	# 4 out of bound questions ["....",first,middle,last,"....."]#	
	save_answer( answer, question_id, tracker, save_order)
	if current_question == question_number:	
		disable_button = "next"
	elif current_question == 1:	
		disable_button = "previous"
  	elif  current_question > 1 and current_question < question_number:
  		disable_button = "none"
  	else:
   		disable_button = "outofbound"
	return 	current_question, disable_button

def generate_random( request ):
	#get grade, topics, branch
	grade = 1
	topics = 2
	branch = 4
	number_of_questions = 10
	user = request.session.__getitem__('uname')		

	classes = SbClass.objects.using('katev').all().order_by("number_view")
#	if request.method == ""
	#topic 1828
	qtype = SbQuestionType.objects.using('katev').filter( short_name__in=( 'single_answer', 'multiple_answer' ))

	questions = SbQuestions.objects.using('katev').filter( grade_id = 2, d_q_type__in = qtype )
	count = questions.count()

	question_ids = []
	for q in questions:
		question_ids.append(q.id)

	qlist = QuizList.objects.create( name='random', number_of_questions=number_of_questions, user=user )

	random_question_ids=[]
	#works like a charm get slice of 	
	if count >= number_of_questions: 	
		random_question_ids = random.sample( question_ids, number_of_questions )
	else:
		for i in range(number_of_questions):
			random_id = random.sample( question_ids, 1 )[0]
			random_question_ids.append( random_id )

	for i in range(number_of_questions):		
		qlist.questioncart_set.create( question = random_question_ids[i] )

	return render( request, "random.html", { "classes":classes, "questions":questions, "random":random_question_ids })