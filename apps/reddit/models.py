from django.db.models import *
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from mptt.models import MPTTModel, TreeForeignKey

@python_2_unicode_compatible
class Thread(Model):
    author = ForeignKey(User)
    title = TextField(default='', max_length=255)
    text = TextField(default='', max_length=1024)
    url = TextField(default='', max_length=1024)

    created_on = DateTimeField(auto_now_add=True)
    votes = IntegerField(default=1)

    def __str__(self):
        short_text = self.title if len(self.title) < 20 else self.title[:18] + '...'
        return '{} by {}'.format(short_text, self.author)


@python_2_unicode_compatible
class Comment(MPTTModel):
    text    = TextField(default = '', max_length = 10000)
    author  = ForeignKey(User, related_name = 'author_of')
    parent  = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    thread = ForeignKey(Thread)

    created_on = DateTimeField(auto_now_add = True)
    updated_on = DateTimeField(auto_now = True)

    votes = IntegerField(default=1)

    class MPTTMeta:
        order_insertion_by = ['votes']

    def __repr__(self):
        return '<Comment %r>' % (self.text[:25])

    def __str__(self):
        return '{} by {}'.format(self.text[:25], self.author)
