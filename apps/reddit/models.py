from django.db.models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from mptt.models import MPTTModel, TreeForeignKey
from slugify import slugify
import re

TITLE_MAXLEN = 128
DESC_MAXLEN = 4096
COMMENT_MAXLEN = DESC_MAXLEN
URL_MAXLEN = 1024
SHORT_NAME_LEN = 20
SHORT_COMMENT_LEN = 128

class Subreddit(Model):
    title = TextField(blank=False, max_length=TITLE_MAXLEN, unique=True)
    desc = TextField(blank=False, max_length=DESC_MAXLEN)

    created_on = DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Subreddit "{}"'.format(self.title)

    def __repr__(self):
        return '<Subreddit {}>'.format(self.id)

    @property
    def slug(self):
        return slugify(self.title, only_ascii=True)

    @property
    def short_title(self):
        if len(self.title) > (SHORT_NAME_LEN - 3):
            sn = self.title[:SHORT_NAME_LEN - 3] + '...'
        else:
            sn = self.title
        return sn


class Thread(Model):
    author = ForeignKey(User)
    title = TextField(blank=False, max_length=TITLE_MAXLEN)
    text = TextField(default='', max_length=DESC_MAXLEN)
    url = TextField(default='', max_length=URL_MAXLEN)
    subreddit = ForeignKey(Subreddit, blank=True, null=True)

    created_on = DateTimeField(auto_now_add=True)
    voters = ManyToManyField(User, related_name='voted_thread')

    def __str__(self):
        short_text = self.title if len(self.title) < 20 else self.title[:18] + '...'
        return '{} by {}'.format(short_text, self.author)

    def __repr__(self):
        return '<Thread {}>'.format(self.id)

    @property
    def slug(self):
        return slugify(self.title, only_ascii=True)

    @property
    def get_comment_number(self):
        return Comment.objects.filter(thread=self).count()

    @property
    def real_url(self):
        return self.url if self.url else self.permalink

    @property
    def permalink(self):
        return reverse('show_thread', kwargs={'thread_id': self.id,
                                              'thread_slug': self.slug,
                                              'subreddit_id': self.subreddit.id,
                                              'subreddit_slug': self.subreddit.slug})

    @property
    def url_type(self):
        is_image = re.search(r'\.(jpg|jpeg|png|gif|gifv|bmp|tiff|tif)$', self.url, flags=re.IGNORECASE)
        if not self.url:
            return 'selfpost'
        elif is_image:
            return 'image'
        else:
            return 'url'

    @property
    def vote_url(self):
        return reverse('vote_thread', kwargs={'thread_id': self.id,
                                              'thread_slug': self.slug,
                                              'subreddit_id': self.subreddit.id,
                                              'subreddit_slug': self.subreddit.slug})


class Comment(MPTTModel):
    text    = TextField(blank=False, max_length=COMMENT_MAXLEN)
    author  = ForeignKey(User, related_name='author_of')
    parent  = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    thread = ForeignKey(Thread)

    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    voters = ManyToManyField(User, related_name='voted_comment')

    class MPTTMeta:
        order_insertion_by = ['created_on']

    def __repr__(self):
        return '<Comment %r>' % (self.text[:25])

    def __str__(self):
        return '{} by {}'.format(self.text[:25], self.author)

    @property
    def comment_level(self):
        return len(self.get_ancestors())

    @property
    def short_text(self):
        if len(self.text) > (SHORT_COMMENT_LEN - 3):
            st = self.text[:SHORT_COMMENT_LEN - 3] + '...'
        else:
            st = self.text
        return st

    @property
    def vote_url(self):
        return reverse('vote_comment', kwargs={'thread_id': self.thread.id,
                                               'thread_slug': self.thread.slug,
                                               'subreddit_id': self.thread.subreddit.id,
                                               'subreddit_slug': self.thread.subreddit.slug,
                                               'comment_id': self.id})
