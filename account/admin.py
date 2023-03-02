from django.contrib import admin
from .models import Stuff
# Register your models here.
class StuffAdmin(admin.ModelAdmin):
    search_fields = ['user', 'role', 'workplace']

    class Meta:
        model = Stuff

admin.site.register(Stuff)