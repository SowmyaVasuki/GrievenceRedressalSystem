from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index,name='index'),
	url(r'^test$', views.test,name='test'),
	url(r'^dashboard/(?P<token>.+)$', views.dashboard,name='dashboard'),
	url(r'^category$', views.Category,name='category'),
	url(r'^category2$', views.Category2,name='category2'),
	url(r'^category3$', views.Category3,name='category3'),
	url(r'^category4$', views.Category4,name='category4'),
	url(r'^category5$', views.Category5,name='category5'),
	url(r'^aform$', views.aform,name='aform'),
	url(r'^sform$', views.sform,name='sform'),
	url(r'^eform$', views.eform,name='eform'),
	url(r'^hform$', views.hform,name='hform'),
	url(r'^oform$', views.oform,name='oform'),
	url(r'^acadconfirm$', views.acad_confirm,name='acad_confirm'),
	url(r'^sportconfirm$', views.sport_confirm,name='sport_confirm'),
	url(r'^eventconfirm$', views.event_confirm,name='event_confirm'),
	url(r'^hostelconfirm$', views.hostel_confirm,name='hostel_confirm'),
	url(r'^othersconfirm$', views.others_confirm,name='others_confirm'),
    url(r'^incharge$', views.incharge,name='incharge'),
    url(r'^ucomp/(?P<har>.+)$', views.usercomp, name="usercomp"),
    url(r'^aupoll/(?P<comid>.+)$', views.aupoll, name="aupoll"),
    url(r'^repoll/(?P<comid>.+)$', views.repoll, name="repoll"),

    
    url(r'^display$', views.retrcomp,name='retrcomp'),
	url(r'^list/(?P<har>.+)$', views.polls_list, name="poll_list"),
	url(r'^edit/(?P<har>.+)/(?P<poll_id>\d+)/$', views.edit_poll, name='edit_poll'),
	url(r'^add/(?P<ident>.+)$', views.add_poll, name='add_poll'),
	url(r'^edit/(?P<har>.+)/(?P<poll_id>\d+)/choice/add$', views.add_choice, name="add_choice"),
	url(r'^edit/choice/(?P<har>.+)/(?P<choice_id>\d+)$', views.edit_choice, name="edit_choice"),
    url(r'^delete/choice/(?P<har>.+)/(?P<choice_id>\d+)$', views.delete_choice, name='choice_confirm_delete'),
    url(r'^delete/poll/(?P<har>.+)/(?P<poll_id>\d+)$', views.delete_poll, name='poll_confirm_delete'),
    # polls/details/1/
    url(r'^details/(?P<poll_id>\d+)$', views.poll_detail, name='detail'),
    # polls/details/1/vote
    url(r'^details/(?P<poll_id>\d+)/vote$', views.poll_vote, name='vote'),
	
]


	
    
    