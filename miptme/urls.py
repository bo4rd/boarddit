from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'miptme.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'apps.reddit.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^thread/(?P<thread_id>[0-9]+)/$', 'apps.reddit.views.show_thread',
        name='thread'),
    url(r'^login/', 'apps.accounts.views.login', name='login'),
    url(r'^logout/$', 'apps.accounts.views.logout', name='logout'),
    url(r'^register/$', 'apps.accounts.views.register', name='register'),
    url(r'^thread/create/$', 'apps.reddit.views.create_thread',
        name='create_thread'),
)
