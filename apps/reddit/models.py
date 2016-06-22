from django.db.models import *
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from mptt.models import MPTTModel, TreeForeignKey
from slugify import slugify

TITLE_MAXLEN = 128
DESC_MAXLEN = 4096
COMMENT_MAXLEN = DESC_MAXLEN
URL_MAXLEN = 1024
SHORT_NAME_LEN = 20

@python_2_unicode_compatible
class Subreddit(Model):
    title = TextField(blank=False, max_length=TITLE_MAXLEN, unique=True)
    desc = TextField(blank=False, max_length=DESC_MAXLEN)

    created_on = DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'Subreddit "{}"'.format(self.title)

    def __repr__(self):
        return u'<Subreddit {}>'.format(self.id)

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


@python_2_unicode_compatible
class Thread(Model):
    author = ForeignKey(User)
    title = TextField(blank=False, max_length=TITLE_MAXLEN)
    text = TextField(default='', max_length=DESC_MAXLEN)
    url = TextField(default='', max_length=URL_MAXLEN)
    subreddit = ForeignKey(Subreddit, blank=True, null=True)

    created_on = DateTimeField(auto_now_add=True)
    votes = IntegerField(default=1)

    def __str__(self):
        short_text = self.title if len(self.title) < 20 else self.title[:18] + '...'
        return u'{} by {}'.format(short_text, self.author)

    def __repr__(self):
        return '<Thread {}>'.format(self.id)

    @property
    def slug(self):
        return slugify(self.title, only_ascii=True)

    @property
    def get_comment_number(self):
        root_comments = Comment.objects.root_nodes().filter(thread=self)
        comment_num = len(root_comments) + sum([comment.children.all().count()
                                                for comment in root_comments])
        return comment_num

    @property
    def real_url(self):
        return self.url if self.url else self.permalink

    @property
    def permalink(self):
        return reverse('apps.reddit.views.show_thread', kwargs={'thread_id': self.id,
                                                                'thread_slug': self.slug,
                                                                'subreddit_id': self.subreddit.id,
                                                                'subreddit_slug': self.subreddit.slug})


@python_2_unicode_compatible
class Comment(MPTTModel):
    text    = TextField(blank=False, max_length=COMMENT_MAXLEN)
    author  = ForeignKey(User, related_name='author_of')
    parent  = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    thread = ForeignKey(Thread)

    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    votes = IntegerField(default=1)

    class MPTTMeta:
        order_insertion_by = ['votes']

    def __repr__(self):
        return '<Comment %r>' % (self.text[:25])

    def __str__(self):
        return u'{} by {}'.format(self.text[:25], self.author)

