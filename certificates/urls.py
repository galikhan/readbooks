from django.conf.urls import url, patterns

urlpatterns = patterns('',
	url(r'^english/$', 'certificates.views.list_english', name= "english"),
	url(r'^computer/$', 'certificates.views.list_computer', name= "computer"),
	url(r'^turkish/$', 'certificates.views.list_turkish', name= "turkish"),

	url(r'^level/$', 'certificates.views.set_level', name= "set_level"),

	url(r'^printcmp/$', 'certificates.views.print_computer', name= "printcmp"),
	url(r'^printtr/$', 'certificates.views.print_turkish', name= "printtr"),
	url(r'^printen/$', 'certificates.views.print_english', name= "printen"),

	url(r'^update_name_surname/$', 'certificates.views.update_name_surname', name= "update_name_surname"),
	url(r'^cert_list/(?P<school>\w+)/$', 'certificates.views.cert_list', name= "cert_list"),
)