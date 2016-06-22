from django.conf.urls import patterns, include, url
from django.contrib import admin

subreddit_patterns = [
    url(r'^$', 'apps.reddit.views.show_subreddit', name='show_subreddit'),
    url(r'^submit/$', 'apps.reddit.views.create_thread', name='create_thread'),
    url(r'^thread/(?P<thread_id>[0-9]+)/(?P<thread_slug>[a-zA-Z0-9_\~\-]+)/$',
        'apps.reddit.views.show_thread', name='show_thread'),
]

urlpatterns = patterns('',
    url(r'^$', 'apps.reddit.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'apps.accounts.views.login', name='login'),
    url(r'^logout/$', 'apps.accounts.views.logout', name='logout'),
    url(r'^register/$', 'apps.accounts.views.register', name='register'),
    url(r'^user/(?P<username>[a-zA-Z0-9]+)/$', 'apps.reddit.views.user_profile', name='user_profile'),
    url(r'^r/(?P<subreddit_id>[0-9]+)/(?P<subreddit_slug>[a-zA-Z0-9_\~\-]+)/', include(subreddit_patterns))
)
