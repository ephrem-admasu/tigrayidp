from django.contrib import admin
from .models import AidItem, AidPackage

# Register your models here.
class AidPackageAdmin(admin.ModelAdmin):
    search_fields = ['package_name', 'distribution_date']

    class Meta:
        model = AidPackage

class AidItemAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category', 'metric', 'allocation_scheme', 'amount', 'aid_package']
    class Meta:
        model = AidItem

admin.site.register(AidItem)
admin.site.register(AidPackage)