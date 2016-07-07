from django.conf.urls import *
from apps.judge import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<contestId>\d+)/problem/(?P<problemId>\d+)/$', views.problem, name='index'),
	url(r'^contest/(?P<contestId>\d+)/$', views.contest, name='index'),
	url(r'^submitsolution/$', views.submitSolution, name='index'),
	url(r'^success/$', views.success, name='index'),
	url(r'^submission/$', views.submission, name='index'),
	url(r'^changePassword/$', views.changePassword, name='index'),
	url(r'^trail/$', views.trial, name='index'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
