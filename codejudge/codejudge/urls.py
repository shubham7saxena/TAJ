from django.conf.urls import *
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

admin.site.site_header = 'CodeJudge-IIT Jodhpur Admin'

urlpatterns = patterns('',
    # Examples:
    url(r'^$', RedirectView.as_view(url='/user/login')),
    url(r'^admin/', admin.site.urls),
    url(r'^judge/', include('apps.judge.urls', namespace="judge")),
    url(r'^user/', include('apps.authentication.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^v1/', include('apps.v1.urls')),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
