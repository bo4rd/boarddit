from __future__ import unicode_literals

from django.db.models import *
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

class Comment(MPTTModel):
    text    = TextField(default = '', max_length = 10000)
    author  = ForeignKey(User, related_name = 'author_of')
    parent  = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    created_on = DateTimeField(auto_now_add = True)
    updated_on = DateTimeField(auto_now = True) 

    votes = IntegerFiled(default=1)
    
    class MPTTMeta:
        order_insertion_by = ['votes']

    def __repr__(self):
        return '<Comment %r>' % (self.text[:25])

    def get_margin_left(self):
        # TODO rework with MPTT
        """
        nested comments are pushed right on a page
        -15px is our default margin for top level comments
        """
        margin_left = 15 + ((self.depth-1) * 32)
        margin_left = min(margin_left, 680)
        return str(margin_left) + "px"

