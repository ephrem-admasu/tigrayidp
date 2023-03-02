from import_export import resources
from .models import FamilyHead, FamilyMember
from datetime import date, datetime, timedelta, timezone
from django.db.models import Q

class FamilyHeadResources(resources.ModelResource):
    class Meta:
        model = FamilyHead
        import_id_fields = ('id_no', )
        exclude = ('id', 'profilepic', 'created_by', 'created', 'updated_by', 'updated', 'aid_packages', 'available')


class ChildrenResources(resources.ModelResource):
    class Meta:
        model = FamilyMember 
    def get_queryset(self):
        qs = FamilyMember.objects.filter(available=True, age_lte = 5)
        return qs 

class ElderlyResources(resources.ModelResource):
    class Meta:
        model = FamilyMember 
    def get_queryset(self):
        qsh = FamilyHead.objects.filter(available=True, age_gte = 60)
        qs = FamilyMember.objects.filter(Q(age__gte = 60) | Q(family_head = qsh), available=True)
        return qs 

class DisabledResources(resources.ModelResource):
    class Meta:
        model = FamilyMember 
    def get_queryset(self):
        qs1 = FamilyMember.objects.filter(available=True, disabled=True)
        qs2 = FamilyMember.objects.filter(available=True, family_head__disabled=True)
        qs = qs1 | qs2
        return qs 

class LactPregnantResources(resources.ModelResource):
    class Meta:
        model = FamilyMember 
        exclude = ('profilepic', 'credence_pic', 'created_by', 'updated_by', 'created', 'updated', )
    def get_queryset(self):
        qs1 = FamilyMember.objects.filter(
            Q(pregnant=True) | Q(family_head__pregnant=True) | Q(lactating = True) | Q(family_head__lactating=True),
            available=True
        )
        # qs2 = FamilyMember.objects.filter(available=True, family_head__pregnant=True)
        # qs = qs1 | qs2
        return qs1

class DuplicateResource(resources.ModelResource):
    class Meta:
        model = FamilyHead
        exclude = (
            'id', 'profilepic', 'created_by', 'created', 'updated_by', 
            'updated', 'aid_packages', 'plw', 'is_idp', 'is_disabled', 
            'psnp_beneficiary', 'emergency_relief_host', 'available',
        )
    def get_queryset(self):
        idps = FamilyHead.objects.all()
        _first = FamilyHead.objects.first()
        qs_all = FamilyHead.objects.filter(full_name__contains = 'UNRECOGNIZED_NAME')
        for idp in idps:
            qs = FamilyHead.objects.filter(full_name__contains = idp.full_name)
            if qs.count() > 1:
                qs_all = qs_all | qs 
        qs_all = qs_all.order_by('full_name')
        return qs_all