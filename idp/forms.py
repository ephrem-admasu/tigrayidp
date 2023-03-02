from django import forms
from .models import FamilyMember, FamilyHead
from .constants import (SUB_CITIES, SITE_CHOICES, REGIONS, OLD_ZONES, OLD_WEREDAS, 
                        CURR_ZONE, TABYAS, SEX, MARITAL_STATUS, RELATION_CHOICES, CREDENCE_TYPE)

class DateInput(forms.DateInput):
    input_type = 'date'

class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember

        exclude = ('family_head', 'updated', 'updated_by')




class FamilyHeadForm(forms.ModelForm):

    class Meta:
        model = FamilyHead

        verbose_name_plural = 'Family Heads'
        exclude = ('updated', 'updated_by', 'is_idp', 'total_hhs', )
