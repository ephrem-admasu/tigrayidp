from django import template
from idp.models import FamilyHead, FamilyMember
from datetime import date, datetime, timedelta, timezone

register = template.Library()


# def is_valid_queryparam(param):
#     return param != '' and param is not None


@register.simple_tag
def num_children():
    qs = FamilyMember.objects.filter(available=True, age__lte = 5)
    return qs.count()

@register.simple_tag
def num_plw():
    qs_m = FamilyMember.objects.filter(available=True, plw=True)
    qs_h = FamilyHead.objects.filter(available=True, plw=True)
    return qs_h.count() + qs_m.count()

# @register.simple_tag
# def num_pregnant():
#     qs_m = FamilyMember.objects.filter(available=True, pregnant=True)
#     qs_h = FamilyHead.objects.filter(available=True, pregnant=True)
#     return qs_h.count() + qs_m.count()

@register.simple_tag
def num_disabled():
    qs_m = FamilyMember.objects.filter(available=True, is_disabled=True)
    qs_h = FamilyHead.objects.filter(available=True, is_disabled=True)
    return qs_h.count() + qs_m.count()

@register.simple_tag
def num_old():
    qs_mem = FamilyMember.objects.filter(available=True, age__gte = 60)
    qs_head = FamilyHead.objects.filter(available=True, age__gte = 60)

    return qs_mem.count() + qs_head.count()

@register.simple_tag
def num_dups():
    idps = FamilyHead.objects.all()
    dups = []
    i = 0
    for idp in idps:
        qs = FamilyHead.objects.filter(full_name__contains = idp.full_name)
        if qs.count() > 1 and qs not in dups:
            dups.append(qs) 
            i = i + 1
    return i 


@register.filter('getsex')
def getsex(var):
    if var.sex == 'Female':
        return 'Herself'
    return 'Himself'

@register.filter('yesno')
def yesno(var):
    if var:
        return 'Yes'
    else:
        return 'No'
@register.filter('isfemale')
def isfemale(var):
    if var.sex=='Female':
        return True
    return False
@register.filter('notsubcityadmin')
def notsubcityadmin(var):
    if var.stuff.role == 'Subcity Socio-Economic Office':
        return False 
    return True 