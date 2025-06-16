from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() or user.is_superuser

@register.filter(name='has_any_group')
def has_any_group(user, groups):
    groups_list = [g.strip() for g in groups.split()]
    return user.groups.filter(name__in=groups_list).exists() or user.is_superuser
