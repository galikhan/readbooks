from django.conf.urls import url ,patterns

urlpatterns = patterns('',
	url(r'^$' , 'online_quiz.views.online_quiz', name="online_quiz"),
	url(r'^quiz/(?P<quiz_id>\d+)/$' , 'online_quiz.views.start_online', name="start_online"),
	url(r'^quiz/(?P<quiz_id>\d+)/(?P<tracker_id>\d+)/$' , 'online_quiz.views.run_online', name="run_online"),
	url(r'^quiz/results/(?P<quiz_id>\d+)/(?P<tracker_id>\d+)/$' , 'online_quiz.views.result_count', name="result_count") ,
	url(r'^quiz/results-show/(?P<quiz_id>\d+)/(?P<tracker_id>\d+)/$' , 'online_quiz.views.result_show', name="result_show") ,
	url(r'^quiz/random/$' , 'online_quiz.views.generate_random', name="random") ,
)