from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'todo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^accounts/login/$', 'tasks.views.login'),
    url('^accounts/logout/$', 'tasks.views.logout'),
    url('^index/$', 'tasks.views.index'),
    url('^tasklist/$', 'tasks.views.tasklist'),
    url('^tasklist/(.+)/$', 'tasks.views.tasklist'),
    url('^taskdetial/(.+)/$', 'tasks.views.taskdetial'),
    url('^taskdetial/$', 'tasks.views.taskdetial'),
    url('^$', 'tasks.views.login'),
)
urlpatterns += staticfiles_urlpatterns()

