from django.conf.urls import patterns, include, url
from mydj import views
from django.contrib import admin
from .models import *
admin.site.register(Question)
admin.site.register(Options)
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mydj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^signup_check', views.signup_check),
    url(r'^login', views.login, name='login'),
    url(r'^home', views.home, name='home'),
    url(r'^create', views.create, name='create'),
    url(r'^polls/(\d+)/$', views.detail),
    url(r'^polls/(\d+)/vote/(\w+)/(\d+)/$', views.vote),
    url(r'^admin/', include(admin.site.urls)),
)
