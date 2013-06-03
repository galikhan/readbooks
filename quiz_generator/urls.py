from django.conf.urls import patterns, url

urlpatterns = patterns("",
	url(r'^topics/$',  "quiz_generator.views.list_topics", name="list_topics"),
	url(r'^topics/(?P<topic_id>\d+)/(?P<subtopic_id>\d+)/$', "quiz_generator.views.list_questions", name="list_questions"),
	url(r'^topics/(?P<topic_id>\d+)/(?P<subtopic_id>\d+)/(?P<index>\d+)/$', "quiz_generator.views.list_questions_by_page", name="list_questions_by_page"),
	url(r'^typeahead/$' , 'quiz_generator.views.typeahead', name = 'typeahead' ),	
	url(r'^add-remove-questions/$', "quiz_generator.views.add_remove_questions_to_cart", name="addremove" ),
	url(r'^create-new-quiz/$', "quiz_generator.views.create_new_quiz", name="create_new_quiz" ),
	url(r'^generate-quiz/$', "quiz_generator.views.generate_quiz", name="generate_quiz" ),
	url(r'^subtopics/$', "quiz_generator.views.load_subtopics", name="load_subtopics" ),
	url(r'^questions/$', "quiz_generator.views.load_questions", name="load_questions" ),

	)
