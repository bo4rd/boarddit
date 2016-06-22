from django import template

register = template.Library()

# Stuff for aligning comment blocks

@register.filter
def comment_notice(level, max_level):
    level, max_level = int(level), int(max_level)
    return 12 - ((level - 1) % max_level) + 1

@register.filter
def comment_notice_offset(level, max_level):
    level, max_level = int(level), int(max_level)
    return ((level - 1) % max_level) + 1

@register.filter
def comment_offset(level, max_level):
    return int(level) % int(max_level)

@register.filter
def comment(level, max_level):
    return 12 - int(level) % int(max_level)
