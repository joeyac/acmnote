"""acmnote2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from acmnote2 import views
from util.captcha.views import show_captcha
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^summernote/', include('django_summernote.urls')),

    url(r'^admin/', admin.site.urls),

    url(r'^$', views.index_page, name='homepage'),

    url(r'^captcha/$', show_captcha, name="show_captcha"),

    url(r'', include('problem.urls')),
    url(r'', include('announcement.urls')),
    url(r'', include('authentication.urls')),
    url(r'', include('note.urls')),
    url(r'', include('group.urls')),
    url(r'', include('submission.urls')),

    # test for myself table columns
    url(r'^table/', include('table.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
