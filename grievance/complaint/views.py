# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import time
# Create your views here.
from django.shortcuts import render
from . models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .forms import PollForm, EditPollForm, ChoiceForm

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import simplejson as json
import random
import smtplib

def index(request):
	template = loader.get_template("complaint/login.html")
	#x = academics.objects.all()
	context = {
	#	'list' : x
	}
	return HttpResponse(template.render(context,request))
def test(request):
	template = loader.get_template("complaint/home.html")
	context = {
		"list" : name,
		"c":Poll.objects.count(),
	}
	return HttpResponse(template.render(context,request))
def dashboard(request,token):
	details = auth_api(token)
	#print(details)
	global name
	global email
	name = details['student'][0]['Student_First_Name']
	email = details['student'][0]['Student_Email']
	rno = details['student'][0]['Student_ID']
	ts = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S") 
	#template = loader.get_template("complaint/home.html")
	Y =Academics.objects.all()
	params=Academics.objects.all()
	if User.objects.filter(UserMailId=email).exists()==False:
		data = User(UserMailId=email,userRollNumber=rno,userName=name,Type = "student",lastloggedin=ts)
		data.save()
	else:
		data = User.objects.get(userName=name)
		data.lastloggedin = ts
		data.save()
	if data.Type == "authority":
		template = loader.get_template("complaint/authority.html")
		pxw = Authority.objects.get(email=email)
		#Yc = pxw.Category#Academics.objects.all()
		Y = checkauth(pxw.Category)
		cat = str(pxw.Category)
		paginator = Paginator(Y, 4)
		page = request.GET.get('page',1)
		Y = paginator.page(page)
		get_dict_copy = request.GET.copy()
		params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
	else:
		template = loader.get_template("complaint/home.html")
		cat = 'hello'
	context = {
		'list' :name,
		'c':Poll.objects.count(),
		"AllList" : Y,
		'params': params,
		'cat' : cat,
	}
	return HttpResponse(template.render(context,request))
def auth_api(token):
    url = ' https://serene-wildwood-35121.herokuapp.com/oauth/getDetails'
    Payload = {'token':token, 'secret':"2e9af1ae7fda17d3d74a125b39348b612f046a6ed5d6b65e1cd01fdeae32da15bdc54b02923b24d7acb3b5ddb995b3a0263cd99f4b021979e40abb1bb2fadff1"}
    s = requests.post(url,Payload)
    details = json.loads(s.content)
    return details
def checkauth(name):
	if name =="Academics":
		return Academics.objects.all()
	if name =="Others":
		return Others.objects.all()
	if name =="Hostel":
		return Hostel.objects.all()
	if name =="Events":
		return Events.objects.all()
	if name =="Sports":
		return Sports.objects.all()
#Incharge
def incharge(request):
	template = loader.get_template("complaint/incharge.html")
	#get the id of current logged in user
	#m = LoggedInUser.objects.all()[0].userId
	#u = User.objects.get(userRollNumber=m)
	#X = u.academics_set.all()
	Y = Academics.objects.all()
	X=Incharge.all_incharges()
	#get the username
	#uname = u.login_set.all()[0].userName
	print("yes")
	print(name)
	context = {
		"uname" : name,
		"list" : X,
	}
	return HttpResponse(template.render(context,request))

def repoll(request,comid):
	template = loader.get_template("complaint/au_poll.html")
	xy = str(comid)
	if xy[0]=='A':
		x= Academics.objects.get(compid=comid)
		x.status=1
		x.save()
	if xy[0]=='E':
		x= Events.objects.get(compid=comid)
		x.status=1
		x.save()
	if xy[0]=='H':
		x= Hostel.objects.get(compid=comid)
		x.status=1
		x.save()
	if xy[0]=='O':
		x= Others.objects.get(compid=comid)
		x.status=1
		x.save()
	if xy[0]=='S':
		x= Sports.objects.get(compid=comid)
		x.status=1
		x.save()
	p="Successfully"
	context = {'success':p,}
	
	return HttpResponse(template.render(context,request))

def aupoll(request,comid):
	template = loader.get_template("complaint/au_poll.html")
	'''u = User.objects.get(UserMailId=email)
	m=u.userRollNumber
	m1 =User.objects.get(userRollNumber=m)'''
	#print(Poll.objects.get(compid=comid))
	try:
		poll = Poll.objects.get(compid=comid,status=0)
		results = poll.get_results_dict()
		context = {'poll': poll, 'results': results}
	except Poll.DoesNotExist:
		poll = None
		p='No Polls Exist'
		context={'exist':p,}
	

	
	
	return HttpResponse(template.render(context,request))

#Academics
def Category(request):
	template = loader.get_template("complaint/academics.html")
	Y = Academics.objects.filter(status=0)[Academics.objects.count()-5:][::-1]
	
	pl = Poll.objects.all()
	pl = pl.filter(compid__icontains='A')
	u = User.objects.get(UserMailId=email)
	paginator = Paginator(Y, 2)
	page = request.GET.get('page',1)
	Y = paginator.page(page)
    
	get_dict_copy = request.GET.copy()
	params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
	context = {
		"uname" : name,
		"AllList" : Y,
		'params': params,
		"c":pl.count(),
		"p":u.academics_set.count(),
	}
	return HttpResponse(template.render(context,request))

#Sports
def Category2(request):
	template = loader.get_template("complaint/sports.html")
	Y = Sports.objects.filter(status=0)[Sports.objects.count()-5:][::-1]
	pl = Poll.objects.all()
	pl = pl.filter(compid__icontains='S')
	u = User.objects.get(UserMailId=email)
	paginator = Paginator(Y, 2)
	page = request.GET.get('page',1)
	Y = paginator.page(page)
	get_dict_copy = request.GET.copy()
	params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
	context = {
		"uname" : name,
		"AllList" : Y,
		'params': params,
		"c":pl.count(),
		"p":u.sports_set.count(),
	}
	return HttpResponse(template.render(context,request))    

#Events
def Category3(request):
	template = loader.get_template("complaint/events.html")
	Y = Events.objects.filter(status=0)[Events.objects.count()-5:][::-1]
	pl = Poll.objects.all()
	pl = pl.filter(compid__icontains='E')
	u = User.objects.get(UserMailId=email)
	paginator = Paginator(Y, 2)
	page = request.GET.get('page',1)
	Y = paginator.page(page)
    
	get_dict_copy = request.GET.copy()
	params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
	context = {
		"uname" : name,
		"AllList" : Y,
		'params': params,
		"c":pl.count(),
		"p":u.events_set.count()
	}
	return HttpResponse(template.render(context,request))

#Hostel
def Category4(request):
	template = loader.get_template("complaint/hostel.html")
	Y = Hostel.objects.filter(status=0)[Hostel.objects.count()-5:][::-1]
	pl = Poll.objects.all()
	pl = pl.filter(compid__icontains='H')
	u = User.objects.get(UserMailId=email)
	paginator = Paginator(Y, 2)
	page = request.GET.get('page',1)
	Y = paginator.page(page)
    
	get_dict_copy = request.GET.copy()
	params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
	context = {
		"uname" : name,
		"AllList" : Y,
		'params': params,
		"c":pl.count(),
		"p":u.hostel_set.count(),
	}
	return HttpResponse(template.render(context,request))    

#Others
def Category5(request):
	template = loader.get_template("complaint/others.html")
	Y = Others.objects.filter(status=0)[Others.objects.count()-5:][::-1]
	pl = Poll.objects.all()
	pl = pl.filter(compid__icontains='O')
	u = User.objects.get(UserMailId=email)
	paginator = Paginator(Y, 2)
	page = request.GET.get('page',1)
	Y = paginator.page(page)
    
	get_dict_copy = request.GET.copy()
	params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
	context = {
		"uname" : name,
		"AllList" : Y,
		'params': params,
		"c":pl.count(),
		"p":u.others_set.count(),
	}
	return HttpResponse(template.render(context,request))


#Academics Register form
def aform(request):
	template = loader.get_template("complaint/acad_register.html")
	#m = LoggedInUser.objects.all()[0].userId
	#u = User.objects.get(userRollNumber=m)
	#uname = u.login_set.all()[0].userName
	context = {
	#	"uname" : uname
	}
	return HttpResponse(template.render(context,request))

#Sports Register form
def sform(request):
	template = loader.get_template("complaint/sport_register.html")
	
	context = {
		
	}
	return HttpResponse(template.render(context,request))

#Events Register form
def eform(request):
	template = loader.get_template("complaint/event_register.html")
	
	context = {
		
	}
	return HttpResponse(template.render(context,request))

#Hostel Register form
def hform(request):
	template = loader.get_template("complaint/hostel_register.html")
	
	context = {
		
	}
	return HttpResponse(template.render(context,request))

#Others Register form
def oform(request):
	template = loader.get_template("complaint/others_register.html")
	
	context = {
		
	}
	return HttpResponse(template.render(context,request))

def usercomp(request,har):
	template = loader.get_template("complaint/usecomp.html")
	#get the id of current logged in user
	#u = User.objects.get(UserMailId=email)
	u = User.objects.get(UserMailId=email)
	if har=='A':
		#X = u.academics_set.filter(status=0)
		X = User.complaintdisplay(email)
	if har=='H':
		X = u.hostel_set.filter(status=0)
	if har=='O':
		X = u.others_set.filter(status=0)
	if har=='S':
		X = u.sports_set.filter(status=0)
	if har=='E':
		X = u.events_set.filter(status=0)
	#X = u.academics_set.all()
	#print("count")
	#print(p)
	context = {
		"uname" : name,
		"list" : X,
		#"p":p,
	}
	return HttpResponse(template.render(context,request))



#Profile settings page

def Mailing(mail,x):
	from_gmail_user = 'grs.sem5@gmail.com'
	from_gmail_password = 'grssem5@123'
	user = mail
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(from_gmail_user, from_gmail_password)
	msg = MIMEMultipart()
	msg['From'] = from_gmail_user
	msg['To'] = user
	msg['Subject'] = "GRS Notification"
	body = "Complaint filed by: " + user + ", description: " + x
	msg.attach(MIMEText(body, 'plain'))
	text = msg.as_string()
	server.sendmail(from_gmail_user, user, text)
	server.quit()

#Academics reg'n confirmation
def acad_confirm(request):
	#get the current logged in user id
	'''px = User.objects.all()
	px = px.order_by('lastloggedin')
	m = px[User.objects.count()-1].userName'''
	u = User.objects.get(UserMailId=email)
	x = request.POST['description']
	stri=str(request.POST['subcat1'])
	p = listsubcat.objects.get(name=stri)
	so = str('A'+str(p.sid)+str(Academics.objects.count() + 1))
	u.academics_set.create(description=x,userId=u.userRollNumber,incharge=p.incharge,subcatId=p.sid,compid=so,fidate=datetime.datetime.now()) 
	u.save()

	Mailing(u.UserMailId,x)

	template = loader.get_template('complaint/acad_register.html')
	V = Academics.objects.get(description=x)
	context = {
		"success" : 'Thanks for submission',
		"confirm" : V,
	}
	return HttpResponse(template.render(context,request))


#Sports reg'n confirmation
def sport_confirm(request):
	'''px = User.objects.all()
	px = px.order_by('lastloggedin')
	m = px[User.objects.count()-1].userName'''
	u = User.objects.get(UserMailId=email)
	x = request.POST['description']
	stri=str(request.POST['subcat'])
	y = request.POST['spname']
	z = request.POST['nat']
	p = listsubcat.objects.get(name=stri)
	so = str('S'+str(p.sid)+str(Sports.objects.count()))
	u.sports_set.create(description=x,userId=u.userRollNumber,sportname=y,nature=z,subcatId=p.sid,compid=so,fidate=datetime.datetime.now()) 
	u.save()

	Mailing(u.UserMailId,x)

	template = loader.get_template('complaint/sport_register.html')
	Xs= Sports.objects.get(description=x)
	context = {
		"success":'Thanks for Submission.',
		"list" : Xs,
		"uname" : name
	}
	return HttpResponse(template.render(context,request))

#Events reg'n confirmation
def event_confirm(request):
	'''px = User.objects.all()
	px = px.order_by('lastloggedin')
	m = px[User.objects.count()-1].userName'''
	u = User.objects.get(UserMailId=email)
	x = request.POST['description']
	stri=str(request.POST['subcat'])
	y = request.POST['ename']
	r = request.POST['nat']
	p = listsubcat.objects.get(name=stri)
	so = str('E'+str(p.sid)+str(Events.objects.count()))
	u.events_set.create(description=x,userId=u.userRollNumber,eventname=y,nature=r,subcatId=p.sid,compid=so,fidate=datetime.datetime.now()) 
	u.save()
	Mailing(u.UserMailId,x)
	template = loader.get_template('complaint/event_register.html')
	
	Xs= Events.objects.get(description=x)
	
	context = {
		"success":'Thanks for Submission.',
		'list': Xs,
		"uname" : name
	}
	return HttpResponse(template.render(context,request))

#Hostel registration confirmation
def hostel_confirm(request):
	'''px = User.objects.all()
	px = px.order_by('lastloggedin')
	m = px[User.objects.count()-1].userName'''
	u = User.objects.get(UserMailId=email)
	x = request.POST['description']
	stri=str(request.POST['subcat'])
	i=request.POST['incharge']
	r=request.POST['roomno']
	p = listsubcat.objects.get(name=stri)
	so = str('H'+str(p.sid)+str(Hostel.objects.count()))
	u.hostel_set.create(description=x,userId=u.userRollNumber,incharge=i,subcatId=p.sid,compid=so,hostelRoomNo=r,fidate=datetime.datetime.now()) 
	u.save()

	Mailing(u.UserMailId,x)

	template = loader.get_template('complaint/hostel_register.html')
	
	Xs= Hostel.objects.get(description=x)
	context = {
		"success":'Thanks for Submission.',
		'list': Xs,
		"uname" : name
	}
	return HttpResponse(template.render(context,request))

#Others reg'n confirmation
def others_confirm(request):
	'''px = User.objects.all()
	px = px.order_by('lastloggedin')
	m = px[User.objects.count()-1].userName'''
	u = User.objects.get(UserMailId=email)
	x = request.POST['description']
	so = str('O'+str(Others.objects.count()))
	u.others_set.create(description=x,userId=u.userRollNumber,compid=so) 
	u.save()

	from_gmail_user = 'grs.sem5@gmail.com'
	from_gmail_password = 'grssem5@123'
	Mailing(u.UserMailId,x)

	template = loader.get_template('complaint/others_register.html')
	
	Xs= Others.objects.get(description=x)
	
	context = {
		"success":'Thanks for Submission.',
		'list': Xs,
		"uname" : name
	}
	return HttpResponse(template.render(context,request))



# Create your views here.

def polls_list(request,har):
    px = User.objects.get(UserMailId=email)
    
    
    ux = px.userRollNumber
    #polls = Poll.objects.all()
    search_term=''
   
    polls = Poll.objects.values('owner__userRollNumber','text','pub_date','vote','compid','id')
    c = polls.count()
    '''if har=='D':
    	polls = list({v['text']:v for v in polls}.values())'''
    
    #print(polls)
    if har != 'D':
    	polls = polls.filter(compid__icontains=har)
    	c = polls.count()
    	#polls = list({v['text']:v for v in polls}.values())
    #print(polls)
    #print(xp)
    #print(type(xp.owner__userRollNumber))
    

    if 'text' in request.GET:
        polls = polls.order_by('text')

    if 'pub_date' in request.GET:
        polls = polls.order_by('-pub_date')

    if 'num_votes' in request.GET:
        polls = polls.annotate(Count('vote')).order_by('-vote__count')

    if 'search' in request.GET:
        search_term = request.GET['search']
        polls = polls.filter(text__icontains=search_term)
    polls = polls.filter(status=0)
    polls = list({v['text']:v for v in polls}.values())
    paginator = Paginator(polls, 2)
    page = request.GET.get('page',1)
    polls = paginator.page(page)
    
    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

    context = {'polls': polls, 'params': params, 'search_term': search_term,'uname':name,'uno':ux,'har':har,'c':c}
    return render(request, 'complaint/polls.html', context)

def checktable(ck):
	print(ck)
	if ck[0]=='A':
		print(ck)
		if Academics.objects.filter(compid=ck):
			return True
	if ck[0]=='H':
		if Hostel.objects.filter(compid=ck):
			return True
	if ck[0]=='O':
		if Others.objects.filter(compid=ck):
			return True
	if ck[0]=='S':
		if Sports.objects.filter(compid=ck):
			return True
	if ck[0]=='E':
		if Events.objects.filter(compid=ck):
			return True
	return False


def add_poll(request,ident):
	if request.method == "POST":
		form = PollForm(request.POST)
		if form.is_valid():
			px = User.objects.get(UserMailId=email)
			
			m=px.userRollNumber
			u = User.objects.get(userRollNumber=m)
			ck = str(form.cleaned_data['compid'])
			
			print(ck[0])
			if ck[0]==ident:
				#print("prefix")
				if checktable(ck):
					#print("added")
					new_poll = form.save(commit=False)
					new_poll.pub_date = datetime.datetime.now()
					new_poll.owner = u
					new_poll.compid = ck
					new_poll.status=0
					new_poll.save()
					new_choice1 = Choice(poll=new_poll,choice_text=form.cleaned_data['choice1']).save()
					new_choice2 = Choice(poll=new_poll,choice_text=form.cleaned_data['choice2']).save()
					messages.success(request,"Poll and Choices added!",extra_tags='alert alert-success alert-dismissible fade show')
					context = {
						'Success':"Poll Successfully Added!!!!!",
						'form':form,
					}
				else:
					form = PollForm()
					context = {
						'fail1':'Please enter valid complaint id',
						'form':form,
					}
			else:
				form = PollForm()
				context = {
					'fail':'Please enter complaint corresponding to the category',
					'form':form,
				}
	else:
		form = PollForm()
		context = {
			'form':form,
		}
	return render(request,'complaint/add_poll.html',context)
@csrf_exempt
def retrcomp(request):
	fromda = request.POST['fromda']
	toda = request.POST['toda']
	pr = Academics.objects.filter(fidate__gt=fromda,fidate__lt=toda)
	print(pr)
	context = {
			'pr':pr,
		}
	return render(request,'complaint/date.html',context)
def edit_poll(request,poll_id,har):
	print(poll_id)
	poll = get_object_or_404(Poll, id = poll_id)
	if request.method == "POST":
		form = EditPollForm(request.POST, instance=poll)
		if form.is_valid():
			form.save()
			messages.success(request,'Poll edited Successfully!',extra_tags='alert alert-success alert-dismissible fade show')
			return redirect('poll_list',har='har')
	else:
		form = EditPollForm(instance=poll)
	return render(request,'complaint/edit_poll.html',{'form':form,'poll':poll,'har':har})




def delete_poll(request, poll_id,har):
    poll = get_object_or_404(Poll, id=poll_id)
    
    if request.method == "POST":
        poll.delete()
        messages.success(
                        request,
                        'Poll Deleted Successfully',
                        extra_tags='alert alert-success alert-dismissible fade show'
                        )
        return redirect('poll_list',har='har')

    return render(request, 'complaint/delete_poll_confirm.html', {'poll':poll,'har':har})





def add_choice(request, poll_id,har):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                            request,
                            'Choice Added Successfully',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('poll_list',har='har')
    else:
        form = ChoiceForm()
    return render(request, 'complaint/add_choice.html', {'form':form,'har':har})


def edit_choice(request, choice_id,har):
    choice = get_object_or_404(Choice, id=choice_id)
    poll = get_object_or_404(Poll, id=choice.poll.id)
    

    if request.method == "POST":
        form = ChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            messages.success(
                            request,
                            'Choice Edited Successfully',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('poll_list',har='har')
    else:
        form = ChoiceForm(instance=choice)
    return render(request, 'complaint/add_choice.html', {'form':form, 'edit_mode': True, 'choice':choice,'har':har})


def delete_choice(request, choice_id,har):
    choice = get_object_or_404(Choice, id=choice_id)
    poll = get_object_or_404(Poll, id=choice.poll.id)
    

    if request.method == "POST":
        choice.delete()
        messages.success(
                        request,
                        'Choice Deleted Successfully',
                        extra_tags='alert alert-success alert-dismissible fade show'
                        )
        return redirect('poll_list',har='har')

    return render(request, 'complaint/delete_choice_confirm.html', {'choice':choice,'har':har})


def poll_detail(request, poll_id):
    
    '''px = User.objects.all()
    px = px.order_by('lastloggedin')
    m=px[User.objects.count()-1].userRollNumber'''
    u = User.objects.get(UserMailId=email)
    m=u.userRollNumber
    m1 =User.objects.get(userRollNumber=m)
    poll = get_object_or_404(Poll, id=poll_id)
    #user_can_vote = poll.user_can_vote(m)
    results = poll.get_results_dict()
    user_votes = m1.vote_set.all()
    qs = user_votes.filter(poll=poll)
    print(qs)
    user_can_vote = poll.user_can_vote(m1)
    print(user_can_vote)
    xyz = Vote.objects.filter(user =m,poll = poll_id)
    #print(xyz)
    
    context = {'poll': poll, 'user_can_vote': user_can_vote, 'results': results}
    return render(request, 'complaint/poll_detail.html', context)


def poll_vote(request, poll_id):
    # try:
    poll = get_object_or_404(Poll, id=poll_id)

    '''if not poll.user_can_vote(request.user):
        messages.error(request, 'Are you crazy? You have already voted on this poll!')
        return redirect('detail', poll_id=poll_id)'''
    px = User.objects.get(UserMailId=email)
    m=px.userRollNumber
    m1 =User.objects.get(userRollNumber=m)
    
    choice_id = request.POST.get('choice')
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        new_vote = Vote(user=m1, poll=poll, choice=choice)
        new_vote.save()
    else:
        messages.error(request, 'No Choice Was Found!')
        return redirect('detail', poll_id=poll_id)
    return redirect('detail', poll_id=poll_id)



