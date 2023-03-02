from django.contrib import admin
from .models import FamilyMember, FamilyHead, Duplicates
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.utils.translation import gettext_lazy as _



class FamilyMemberInline(admin.StackedInline):
    model = FamilyMember
    raw_id_fields = ['family_head']



class FamilyHeadAdmin(ImportExportModelAdmin):
    list_display = (
        'full_name', 'age', 'sex', 'phone_no', 'marital_status', 
        'region', 'ozone', 'owereda', 'okebele',
        'czone', 'cwereda', 'ckebele',
        'idp_site', 'year_fled'
        )
    list_display_links = ('full_name', )
    list_per_page = 50
    search_fields = ('full_name', 'phone_no', 'marital_status')
    list_filter = (
        'created', 'sex', 'age', 'region', 'ozone', 'owereda', 'okebele',
        'czone', 'cwereda', 'ckebele', 'idp_site', 'year_fled', 
        'plw', 'is_idp', 'is_disabled', 'psnp_beneficiary', 'emergency_relief_host', 'available'
    )
    inlines = [FamilyMemberInline]

    class Meta:
        model = FamilyHead



class FamilyMemberAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'age', 'sex', 'family_head', 'relation', 'credence', 'credence_pic')
    list_per_page = 50
    list_display_links = ('full_name', 'family_head', )
    search_fields = ('full_name', 'relation', 'marital_status')
    list_filter = (
        'created', 'sex', 'age', 'available', 'plw', 'is_disabled', 'is_disabled', 
        'family_head__region', 'family_head__cwereda', 'family_head__ckebele'
    )
    class Meta:
        model = FamilyMember

class DuplicatesAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'age', 'sex', 'phone_no', 'region', 'ozone', 'owereda', 'okebele', 
        'cwereda', 'ckebele', 'idp_site', 'household_head'
    )
    search_fields = ['full_name', 'sex', 'ozone', 'owereda', 'cwereda', 'ckebele']
    class Meta:
        model = Duplicates

# class AidQuotaAdmin(admin.ModelAdmin):
#     search_fields = ['family', 'aid_round', 'status', 'approved_by']
#     class Meta:
#         model = AidQuota 




# admin.site.register(Address, AddressAdmin)
admin.site.register(FamilyHead, FamilyHeadAdmin)
admin.site.register(FamilyMember, FamilyMemberAdmin)
admin.site.register(Duplicates, DuplicatesAdmin)
# admin.site.register(AidRound)
# admin.site.register(AidQuota)