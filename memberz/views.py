from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import Context, loader
from django import  forms 
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.template import loader, RequestContext
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from memberz.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.template.response import TemplateResponse
import datetime


current_year = datetime.datetime.now() 
two_weeks    = datetime.datetime.now() - datetime.timedelta(days=14)


#login -STEPHEN
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '    Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '    Enter your password'}))


@csrf_exempt
def do_login(request):
	empty_cred = '' #empty login credential variable
	disabled_accMsg = ''
	invalidMsg = ''
        already_logged_in = ''
        
			
	if request.user.username != '' and request.user.is_active:
		return HttpResponseRedirect('/home')

	
	
	if request.method == 'POST':
   	        uname = request.POST['username']	
		pword = request.POST['password']
		if uname == '' or pword == '':
			empty_cred = 'Username or password field cannot be empty!'
		else:
			user = authenticate(username=uname, password=pword)
			#if user.is_staff:
			if user is not None:
				if user.is_active:
			        	login(request,user)
					request.session["sess_uname"] = uname
					return HttpResponseRedirect('/home')
				else:
					disabled_accMsg = "Sorry, your account has been disabled. Contact the administrator."
					
			else:
				invalidMsg = "Username or Password is invalid!"
			#else:
				#disabled_accMsg = "Sorry, your account has been disabled. Contact the administrator."
			#return an invalid login message
	
		#YOUR CODE HERE
	else:
		form = LoginForm()
	form = LoginForm()
	return render_to_response('login/signin.html', {
        'form': form,
        'logged_in': request.user.is_authenticated(),
	'invalidMsg': invalidMsg,
	'empty_cred':empty_cred,
	'disabled_accMsg': disabled_accMsg,
	'user': request.user
        
    })



   
@csrf_exempt
def do_logout(request):
	if request.user.username == '' or request.user.is_active == False:
		request.user.username = ''
		request.session["sess_uname"] = ''
		return HttpResponseRedirect('/')
	try:
    		if request.user.username != '':
			logout(request)
			request.session["sess_uname"] = ''
			request.user.username == ''
			return HttpResponseRedirect('/')
    
		else:
			
			return HttpResponseRedirect('/home')
		

        except KeyError:
		logout(request)
		request.session["sess_uname"] = ''
		request.user.username == ''
		return HttpResponseRedirect('/')
		

def home(request):
	if request.user.username == '' or request.user.is_active == False:
		request.user.username = ''
		request.session["sess_uname"] = ''
		return HttpResponseRedirect('/')
	else:
		male_memberz  = member.objects.filter(year__year__gte = int(current_year.strftime("%G")),sex = "Male",completed =False)
                female_memberz  = member.objects.filter(year__year__gte = int(current_year.strftime("%G")),sex = "Female",completed =False)
                memberz  = member.objects.filter(year__year__gte = int(current_year.strftime("%G")),completed =False)
                completed_memberz  = member.objects.filter(year__year__lt = int(current_year.strftime("%G")))
                alumni_memberz     = member.objects.filter(completed =True)
                completed_list      = []
                for memb in completed_memberz:
                    completed_list.append(memb) 
                for memb in alumni_memberz:
                    completed_list.append(memb)
                alumni       =  list(set(completed_list))
                noy_memberz  = member.objects.filter(year =None)
                new_memberz  = member.objects.filter(date_added__gte = two_weeks )
                nol_memberz  = member.objects.filter(year__year__gte = int(current_year.strftime("%G")),level= None,completed =False)
		memberz_100  = member.objects.filter(year__year__gte = int(current_year.strftime("%G")),level="100",completed =False)
                memberz_200  = member.objects.filter(year__year__gte = int(current_year.strftime("%G")),level="200",completed =False)
                memberz_300  = member.objects.filter(year__year__gte = int(current_year.strftime("%G")),level="300",completed =False)
                memberz_400  = member.objects.filter(year__year__gte = int(current_year.strftime("%G")),level="400",completed =False)
		return render_to_response('portal/base.html', {'memberz':memberz,'noy_memberz':noy_memberz,
								'male_memberz':male_memberz,
							        'female_memberz':female_memberz,
								'completed_memberz':completed_memberz,
                                                                'memberz_100':memberz_100,
        							'memberz_200':memberz_200,
                                                                'memberz_300':memberz_300,
                                                                'memberz_400':memberz_400,'alumni':alumni,'alumni_memberz':alumni_memberz,
                                                                'nol_memberz':nol_memberz,'new_memberz':new_memberz,
								'user': request.user})

def memberz(request):
     if request.user.username == '' or request.user.is_active == False:
		request.user.username = ''
		request.session["sess_uname"] = ''
		return HttpResponseRedirect('/')
     else:      
                memberz  = member.objects.filter(year__year__gte = int(current_year.strftime("%G")),completed =False)
		paginator = Paginator(memberz, 10)
		page = request.GET.get('page')
     try:
            memberz = paginator.page(page)
     except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            memberz = paginator.page(1)
     except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            memberz = paginator.page(paginator.num_pages)
     members  = member.objects.filter(year__year__gte = int(current_year.strftime("%G")),completed =False)
     return render_to_response('portal/memberz.html', {'memberz':memberz,'members':members,'user': request.user})

def search(request,term):
	memberz = ''
        if request.user.username == '':
		return HttpResponseRedirect('/')
		
	else:
		if request.GET.get('search_item','') != '':
			term = request.GET.get('search_item','')
			memberz = str(term)
	       		crew = member.objects.filter(index_number__icontains=term)|member.objects.filter(surname__icontains=term)|member.objects.filter(other_name__icontains=term)|member.objects.filter(phone_number__icontains=term)
	       		krew = crew
	       		paginator = Paginator(crew, 10)
		        page = request.GET.get('page')
		       
		        
	        else: 
	        	krew = member.objects.filter(index_number__icontains=memberz)|member.objects.filter(surname__icontains=memberz)|member.objects.filter(other_name__icontains=memberz)|member.objects.filter(phone_number__icontains=memberz)
	      		paginator = Paginator(krew, 10)
		        page = request.GET.get('page')
		        crew = krew
	      		
        
    	try:
            crew = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            crew = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            crew = paginator.page(paginator.num_pages)
        
        current_member 	= member.objects.filter(year__year__gte = int(current_year.strftime("%G")),completed =False)
	return render_to_response('portal/search.html',{
					'crew':crew,'krew':krew,
					'term':term,'current_member':current_member,
					'user':request.user})

