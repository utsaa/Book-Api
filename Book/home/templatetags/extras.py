from django import template

register=template.Library()
@register.filter(name='get_title')
def get_title(x):
    ans= x['volumeInfo'].get('title',None)
    return ans if ans else ""

@register.filter(name='get_auth')
def get_auth(x):
    ans= x['volumeInfo'].get('authors',None)
    return ', '.join(ans) if ans  else ""

@register.filter(name='get_pg')
def get_pg(x):
    ans= x['volumeInfo'].get('pageCount',None)
    if ans=="None": return 0
    return ans if ans else 0

@register.filter(name='get_rating')
def get_rating(x):
    ans= x['volumeInfo'].get('averageRating',None)
    if ans=="None": return 0
    return ans if ans else 0