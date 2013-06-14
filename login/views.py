from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from login.forms import LoginForm
from django.shortcuts import render_to_response, render, get_object_or_404
from readbooks.views import *
#import replace
from django.core.urlresolvers import reverse
import datetime
from readbooks.models import ReadMore
from django.db.models import *

def test_translate(request):
	i = request.LANGUAGE_CODE
	
	output = _("simple")
	output2 = ugettext("simple")
	return HttpResponse(output+" | "+i+" | "+output2)

def user_login(request):

	#if i logged as admin user authentication will not work correctly

	if request.user.is_authenticated():
		return HttpResponseRedirect("/welcome/")
	else:
		if request.method == "POST":
			login_form = LoginForm(request.POST)
			if login_form.is_valid():

				u = login_form.cleaned_data['username']
				p = login_form.cleaned_data['password']
				try:		
					user = authenticate(username=u, password=p)
				except ValueError:
					return render(request, "login.html", {"login_form":login_form, "error_msg": "You entered incorrect username or password !" })
				
			
				if user is None:
					return render(request, "login.html", {"login_form":login_form, "error_msg": "You entered incorrect username or password !" })

				else:
					if user.is_active:
						login(request, user)
						return HttpResponseRedirect("/welcome/")	
					else:
						return render(request, "login.html", {"login_form":login_form, "error_msg": "Your Account Disabled." })
					
			else:
				return render(request, "login.html", {"login_form":login_form})
		
		else:
			login_form = LoginForm()
			return render(request, "login.html", {"login_form":login_form})

def user_logout(request):
	logout(request)
	return HttpResponseRedirect("/")


def welcome(request):

	if request.user.is_authenticated() and not request.user.username == 'admin' :

		u = request.user.username
		u = u.replace('ktl', '')	
		u = u.replace('katev', '')

		user_profile = get_object_or_404( TeacherProfile, teacher_id = u )

		request.session.__setitem__('uname', u)
		request.session.__setitem__('branch', user_profile.branch_id)
		request.session.__setitem__('school', user_profile.school_id)
		readmore = ReadMore.objects.values("book__name","book__isbn","book__bookimage").annotate( buk=Count("book__isbn")).order_by("-buk")[:5]

		#Because of certificates view was changed
		#return render(request ,"welcome.html", {"u":user_profile, "booklist": readmore, "query":readmore.query },)	
		return HttpResponseRedirect(reverse("certificates.views.list_computer"))
	else:
		user_logout(request)	

	return HttpResponseRedirect("/")


	
