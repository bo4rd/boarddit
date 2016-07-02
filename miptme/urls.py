from django.conf.urls import patterns, include, url
from django.contrib import admin
import apps.reddit.views as reddit_views
import apps.accounts.views as accounts_views

thread_patterns = [
    url(r'^$', reddit_views.show_thread, name='show_thread'),
    url(r'comment_tree/(?P<comment_id>[0-9]+)/$',
        reddit_views.show_thread, name='comment_tree'),
]

subreddit_patterns = [
    url(r'^$', reddit_views.show_subreddit, name='show_subreddit'),
    url(r'^submit/$', reddit_views.create_thread, name='create_thread'),
    url(r'^thread/(?P<thread_id>[0-9]+)/(?P<thread_slug>[a-zA-Z0-9_\~\-\']+)/',
        include(thread_patterns)),
]

urlpatterns = [
    url(r'^$', reddit_views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', accounts_views.login, name='login'),
    url(r'^logout/$', accounts_views.logout, name='logout'),
    url(r'^register/$', accounts_views.register, name='register'),
    url(r'^user/(?P<username>[a-zA-Z0-9]+)/$', accounts_views.user_profile, name='user_profile'),
    url(r'^r/(?P<subreddit_id>[0-9]+)/(?P<subreddit_slug>[a-zA-Z0-9_\~\-\']+)/',
        include(subreddit_patterns))
]
