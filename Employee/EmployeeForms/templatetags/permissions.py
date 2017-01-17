from django import template
from django.contrib.auth.models import Group
from django.conf import settings

register = template.Library()



@register.filter(name='has_group')  # added for grievance admin module
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except group.DoesNotExist:
        group = None
    return True if group in user.groups.all() else False

