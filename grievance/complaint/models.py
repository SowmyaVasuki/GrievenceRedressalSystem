# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import connection
from django.db import models
import datetime
# Create your models here.
class User(models.Model):
	userRollNumber = models.BigIntegerField(unique=True)
	userName = models.CharField(max_length = 45)
	UserMailId = models.CharField(max_length = 45,default="@iiits.in")
	Type = models.CharField(max_length = 45,default="None")
	lastloggedin = models.DateTimeField()
	
	def __str__(self):
		return str(self.userRollNumber)
	@staticmethod
	def complaintdisplay(UserMailId):  
        # create a cursor
		cur = connection.cursor()  
        # execute the stored procedure passing in   
        # search_string as a parameter
		cur.callproc('complaintdisplay', [UserMailId,])  
        # grab the results
		columns = [col[0] for col in cur.description]
		results= [
			dict(zip(columns, row))
			for row in cur.fetchall()
        ]
        #results = cur.fetchall()
        # print("****")
        # print(len(results))
		cur.close()  
        # wrap the results up into Document domain objects
		return results

class Incharge(models.Model):
	inchargeId = models.AutoField(primary_key=True)
	inchargeName = models.CharField(max_length=45)
	SubCategory = models.CharField(max_length=45)
	email = models.CharField(max_length = 45, default="@iiits.in")

	def __str__(self):
		return str(self.inchargeName)
	@staticmethod
	def all_incharges():  
        # create a cursor
		cur = connection.cursor()  
        # execute the stored procedure passing in   
        # search_string as a parameter
		cur.callproc('all_incharges')  
        # grab the results
		columns = [col[0] for col in cur.description]
		results= [
			dict(zip(columns, row))
			for row in cur.fetchall()
        ]
        #results = cur.fetchall()
        # print("****")
        # print(len(results))
		cur.close()  
        # wrap the results up into Document domain objects
		return results

class Authority(models.Model):
	authId = models.AutoField(primary_key=True)
	authName = models.CharField(max_length=45)
	Category = models.CharField(max_length=45)
	email = models.CharField(max_length = 45, default="@iiits.in")

	def __str__(self):
		return str(self.authName)

class Academics(models.Model):
	acadId = models.AutoField(primary_key=True)
	userId = models.ForeignKey(User, on_delete = models.CASCADE)
	subcatId = models.IntegerField(default=0)
	incharge = models.CharField(max_length=45)
	description = models.CharField(max_length = 400)
	compid = models.CharField(max_length=15,default='R')
	fidate = models.DateField(default = datetime.datetime(2018,11,9))
	status = models.IntegerField(default=0)

	def __str__(self):
		return 'ComplaintId:' + str(self.compid)+ "	" + ' Incharge: ' + str(self.incharge) + "	"+' description: ' + str(self.description)

class latestOtp(models.Model):
	userId = models.ForeignKey(User, on_delete = models.CASCADE)
	otp = models.IntegerField()

class Sports(models.Model):
	sportsId = models.AutoField(primary_key=True)
	userId = models.ForeignKey(User, on_delete = models.CASCADE)
	subcatId = models.IntegerField(default=0)
	sportname = models.CharField(max_length=45)
	nature = models.CharField(max_length=45)
	description = models.CharField(max_length = 400)
	compid = models.CharField(max_length=15,default='R')
	fidate = models.DateField(default = datetime.datetime(2018,11,9))
	status = models.IntegerField(default=0)

	def __str__(self):
		return 'ComplaintId:'+ str(self.compid) + "	"+ ' Sportname: ' + str(self.sportname) + "		"+ ' description: ' + str(self.description)

class Events(models.Model):
	eventId = models.AutoField(primary_key=True)
	userId = models.ForeignKey(User, on_delete = models.CASCADE)
	subcatId = models.IntegerField(default=0)
	eventname = models.CharField(max_length=45)
	#fromdate = models.DateTimeField()
	#todate = models.DateTimeField()
	nature = models.CharField(max_length=45)
	description = models.CharField(max_length = 400)
	status = models.IntegerField(default=0)
	compid = models.CharField(max_length=15,default='R')
	fidate = models.DateField(default = datetime.datetime(2018,11,9))


	def __str__(self):
		return 'ComplaintId:' + str(self.compid)+ " "+' Eventname: ' + str(self.eventname) +"	"+ ' description: ' + str(self.description)

class Hostel(models.Model):
	hostelId = models.AutoField(primary_key=True)
	userId = models.ForeignKey(User, on_delete = models.CASCADE)
	subcatId = models.IntegerField(default=0)
	incharge = models.CharField(max_length=45)
	hostelRoomNo = models.CharField(max_length=6)
	description = models.CharField(max_length = 400)
	compid = models.CharField(max_length=15,default='R')
	fidate = models.DateField(default = datetime.datetime(2018,11,9))
	status = models.IntegerField(default=0)


	def __str__(self):
		return 'ComplaintId:' + str(self.compid) +"	" +' description: ' + str(self.description)

class Others(models.Model):
	othersId = models.AutoField(primary_key=True)
	userId = models.ForeignKey(User, on_delete = models.CASCADE)
	description = models.CharField(max_length = 400)
	compid = models.CharField(max_length=15,default='R')
	fidate = models.DateField(default = datetime.datetime(2018,11,9))
	status = models.IntegerField(default=0)


	def __str__(self):
		return 'ComplaintId:' + str(self.compid)+"	" + ' description: ' + str(self.description)


class listsubcat(models.Model):
	sid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=45)
	incharge = models.CharField(max_length=45,default="xwq")
	catid = models.IntegerField(default=0)

#Create Polls
class Poll(models.Model):
    owner = models.ForeignKey(User,to_field='userRollNumber', on_delete=models.CASCADE)
    compid = models.CharField(max_length=45)
    text = models.CharField(max_length=255)
    pub_date = models.DateField()
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    def user_can_vote(self, user):
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def num_votes(self):
        return self.vote_set.count()

    def get_results_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            d['text'] = choice.choice_text
            d['num_votes'] = choice.num_votes
            if not self.num_votes:
                d['percentage'] = 0
            else:
                d['percentage'] = choice.num_votes / self.num_votes * 100
            res.append(d)
        return res


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE,default=1)
    choice_text = models.CharField(max_length=255,default="choice")

    def __str__(self):
        return "{} - {}".format(self.poll.text[:25], self.choice_text[:25])

    @property
    def num_votes(self):
        return self.vote_set.count()

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)