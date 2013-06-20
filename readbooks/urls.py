from django.conf.urls import patterns, include, url
from views import *
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    #the first called view after authentication "welcome"
    url(r'^welcome/$', 'login.views.welcome', name="welcome"),

    url(r'^trans/$', 'login.views.test_translate', name='trans'),
	
    url(r'^import/$', 'readbooks.views.import_all', name='import'),
    url(r'^importbranch/$', 'readbooks.views.import_branch', name='importbranch'),
    url(r'^create/$', 'readbooks.views.create_users', name='create_users'),

    url(r'^$', 'login.views.user_login', name="login"),
    url(r'^logout/$', 'login.views.user_logout', name="logout"),

	url(r'^book/all$', 'readbooks.views.viewallbooks', name="viewall"),
    url(r'^book/$', 'login.views.addbook', name="addbook"),
    url(r'^book/(?P<bookid>\d+)/$', 'login.views.bookcontent', name="bookcontent"),

    url(r'^course/$', 'readbooks.views.createcourse', name="createcourse"),
    url(r'^course/all/(?P<grade>\d+)/$', 'readbooks.views.allcoursebooks', name="allcoursebooks"),
    url(r'^course/(?P<grade>\d+)/$', 'readbooks.views.editcoursegrade', name="editcoursegrade"),

    url(r'^course/(?P<grade>\d+)/(?P<search>(.+))/$', 'readbooks.views.afterbookadded', name="afterbookadded"),

    url(r'^add/(?P<grade>\d+)/(?P<bookid>\d+)/(?P<search>(.+))/$', 'readbooks.views.addcoursebook',name="addcoursebook"),

#/book.id/search
#   url(r'^course/(?P<grade>\d+)/(?P<search>([A-z0-9]+))/$', 'login.views.afterbookadded', name="afterbookadded"),
#   url(r'^course/(?P<grade>\d+)/(?P<bookid>\d+)/(?P<search>([A-z0-9]+))/$', 'login.views.addcoursebook', name="addcoursebook"),

    url(r'^delete/(?P<gradeindex>\d+)/(?P<bookid>\d+)/$', 'login.views.deletefromlist', name="deletefromlist"),

    url(r'^results/$', 'readbooks.views.fillresults', name="fillresults"),
    url(r'^results/(?P<gradeindex>\d+)/$', 'readbooks.views.studentslist', name="studentslist"),

    url(r'^saveresult/$', 'readbooks.views.savebookred', name="savebookred" ),

    url(r'^statistics/$', 'statistics.views.statistics', name="statistics" ),
    url(r'^statistics/(?P<gradeindex>\d+)/$', 'statistics.views.statisticsparams', name="statisticsparam" ),

    url(r'^treejs/$', 'treejs.views.home', name="treehome" ),
 

    url(r'^quiz/', include('quiz_generator.urls')),
    url(r'^rating/', include('questionrating.urls')),
    url(r'^online/', include('online_quiz.urls')),
    url(r'^cert/', include('certificates.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
