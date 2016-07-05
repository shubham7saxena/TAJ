from django.conf.urls import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url='/user/login')),
	url(r'^login/$', views.userLogin, name='index'),
	url(r'^logout/$', views.userLogout, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^profile/$', views.profile, name='index'),
	url(r'^changepic/$', views.changeProfilePic, name='index'),
	url(r'^removepic/$', views.removeProfilePic, name='index'),
	url(r'^editProfile/$', views.editProfile, name='index'),
	url(r'^editUser/$', views.editUser, name='index'),
	url(r'^changePassword/$', views.changePassword, name='index'),
	url(r'^newUser/$', views.newUser, name='index'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
