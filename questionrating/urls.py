from django.conf.urls import url, patterns

urlpatterns = patterns('', 
    url(r'^$', 'questionrating.views.two_week_old_questions', name='rating'),
    url(r'^save-rating/$', 'questionrating.views.save_question_rating', name='save_rating'),
)
