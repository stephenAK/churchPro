from django.conf.urls.defaults import *
from memberz.views import *


urlpatterns = patterns('',
		url(r'^$', 'memberz.views.do_login'),
		url(r'^logout/$', 'memberz.views.do_logout'),
                url(r'^home/$', 'memberz.views.home'),
		url(r'^memberz/$', 'memberz.views.memberz'),
                url(r'^search/memberz/(?P<term>.*?)$','memberz.views.search'),
                
)
