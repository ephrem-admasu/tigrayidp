from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from aid.models import AidPackage
from django.urls import reverse
from datetime import date, datetime, timedelta, timezone
from .constants import (SUB_CITIES, SITE_CHOICES, REGIONS, OLD_ZONES, OLD_WEREDAS, 
                        CURR_ZONE, TABYAS, SEX, MARITAL_STATUS, RELATION_CHOICES, CREDENCE_TYPE)
# Create your models here.




class FamilyHead(models.Model):
    id_no = models.CharField('ID No. ', max_length=15, unique=True, blank=True, null=True)
    full_name = models.CharField('Name: ', max_length = 100, null=True)
    profilepic = models.ImageField('Profile Pic.', upload_to = 'idp/img', blank=True, null=True)
    sex = models.CharField('Sex: ', max_length=8, choices = SEX, null=True)
    age = models.PositiveIntegerField('Age', default=0)
    male_hhs = models.PositiveIntegerField('Male HH Size', null=True)
    female_hhs = models.PositiveIntegerField('Female HH Size', null=True)
    total_hhs = models.PositiveIntegerField('Tota HH Size', null=True)
    phone_no = models.CharField('Phone No. ', max_length=20, blank=True, null=True)
    marital_status = models.CharField('Marital Status', max_length=20, choices = MARITAL_STATUS, null=True)
    region =  models.CharField('Prev. Region', max_length=20, choices = REGIONS)
    ozone = models.CharField('Prev. Zone', max_length=20, choices = OLD_ZONES)
    owereda = models.CharField('Prev. Woreda', max_length=20, choices = OLD_WEREDAS)
    okebele = models.CharField('Prev. Kebele', max_length=20)
    czone = models.CharField('Current Zone', max_length=20, choices=CURR_ZONE)
    cwereda = models.CharField('Current Subcity', max_length=20, choices=SUB_CITIES)
    ckebele = models.CharField('Current Subcity', max_length=20, choices=TABYAS, blank=True, null=True)
    idp_site =  models.CharField('IDP Site', max_length=20)
    year_fled = models.PositiveIntegerField('Year Fled', null=True)
    plw = models.BooleanField('Pregnant or Lactating', default=False)
    is_idp = models.BooleanField('Is IDP?', default=False)
    is_disabled = models.BooleanField('Disabled?', default=False)
    psnp_beneficiary = models.BooleanField('PSNP Beneficiary', default=False)
    emergency_relief_host = models.BooleanField('Emergency Relief Host', default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by=models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, 
        null=True, related_name='updated_by_head'
    )
    created_by=models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, 
        null=True, related_name='created_by_head'
    )
    available = models.BooleanField(default=True)
    # aid_packages = models.ManyToManyField(AidPackage, related_name='aid_seekers', blank=True, default=None)

    class Meta:
        ordering = ('-created', '-updated', )

    def __str__(self):
        return self.full_name
    
    def get_absolute_url(self):
        return reverse(
            "idp:detail", 
            kwargs={
                'id':self.id
            }
        )


    

    def family_size(self):
        qs = FamilyMember.objects.filter(family_head=self)
        return qs.count() + 1

    def family_size_male(self):
        qs = FamilyMember.objects.filter(family_head=self, sex = 'Male')
        cnt = qs.count()
        if self.sex == 'Male':
            cnt = cnt + 1
        return cnt 
    def family_size_female(self):
        return self.family_size() - self.family_size_male()
   
    def children_perc(self):
        qs = FamilyMember.objects.filter(family_head=self, available=True, age__lte = 5).count()
        return 1 + qs/self.family_size()

    def disabled_perc(self):
        dis_count = FamilyMember.objects.filter(family_head=self, available=True, is_disabled=True).count()
        if self.is_disabled:
            dis_count += 1
        
        return 1 + dis_count/self.family_size()

    def lact_pregnant_perc(self):
        preg_count = FamilyMember.objects.filter(family_head=self, available=True, plw=True).count()
        if self.plw:
            preg_count += 1
        
        return 1 + preg_count/self.family_size()

    def female_perc(self):
        female_count = FamilyMember.objects.filter(family_head=self, available=True, sex='Female').count()
        if self.sex == 'Female':
            female_count += 1
        
        return 1 + female_count/self.family_size()

    # def lactating_perc(self):
    #     lact_count = FamilyMember.objects.filter(family_head=self, available=True, lactating=True).count()
    #     if self.lactating:
    #         lact_count += 1
        
    #     return 1 + lact_count/self.family_size()
        
    def elderly_perc(self):
        eld_count = FamilyMember.objects.filter(family_head=self, available=True, age__gte = 60).count()
        if self.age and self.age >= 60:
            eld_count += 1
        return 1 + eld_count/self.family_size()
    
    def family_priority(self):
        priority = 0.0
        for p in self.aid_packages.all():
            if p.target_group == 'Family':
                priority -= 1
        priority += (.25 * self.children_perc() + .20*self.elderly_perc() + .25*self.disabled_perc() + .15*(self.lact_pregnant_perc() + self.female_perc()))
        return priority    

    def priority_calc(self, val, group):
        priority = 0.0
        for p in self.aid_packages.all():
            if p.target_group == group:
                priority -= 1
        return val + priority

    def children_priority(self):
        return self.priority_calc(self.children_perc(), 'Children')
    def lact_pregnant_priority(self):
        return self.priority_calc(self.pregnant_perc(), 'Pregnant or Lactating')
    def elderly_priority(self):
        return self.priority_calc(self.elderly_perc(), 'Elderly')
    def disabled_priority(self):
        return self.priority_calc(self.disabled_perc(), 'Disabled')
    def lactating_priority(self):
        return self.priority_calc(self.lactating_perc(), 'Lactating')



class FamilyMember(models.Model):
    full_name = models.CharField('Full Name', max_length = 100)
    profilepic = models.ImageField('Profile Pic.', upload_to = 'idp/img', blank=True)
    sex = models.CharField('Sex: ', max_length=8, choices = SEX)
    age = models.PositiveIntegerField('Age')
    marital_status = models.CharField('Marital Status', max_length = 15, choices = MARITAL_STATUS)
    family_head = models.ForeignKey(FamilyHead, related_name="members", blank=True, on_delete=models.PROTECT)
    relation = models.CharField(max_length = 20, choices = RELATION_CHOICES)
    credence = models.CharField(max_length=50, choices = CREDENCE_TYPE)
    credence_pic = models.ImageField(upload_to = 'idp/img', blank=True)
    plw = models.BooleanField('Pregnant or Lactating', default=False)
    is_disabled = models.BooleanField('Disabled?', default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by=models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, 
        null=True, related_name='updated_by_member'
    )
    created_by=models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, 
        null=True, related_name='created_by_member'
    )
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created', '-updated', )

    def __str__(self):
        return self.full_name
    
class Duplicates(models.Model):
    full_name = models.CharField('Full Name', max_length = 100) 
    sex = models.CharField('Sex: ', max_length=8, choices = SEX, null=True)
    age = models.PositiveIntegerField('Age', null=True)
    phone_no = models.CharField('Phone No. ', max_length=20, blank=True, null=True)
    region =  models.CharField('Prev. Region', max_length=15, choices = REGIONS)
    ozone = models.CharField('Prev. Zone', max_length=15, choices = OLD_ZONES)
    owereda = models.CharField('Prev. Woreda', max_length=15, choices = OLD_WEREDAS)
    okebele = models.CharField('Prev. Kebele', max_length=10)
    czone = models.CharField('Current Zone', max_length=15, choices=CURR_ZONE)
    cwereda = models.CharField('Current Subcity', max_length=15, choices=SUB_CITIES)
    ckebele = models.CharField('Current Tabyas/Kebeles', max_length=15, choices=TABYAS)
    idp_site =  models.CharField('IDP Site', max_length=20)
    cleared = models.BooleanField('Pregnant or Lactating', default=False)
    household_head = models.ForeignKey(FamilyHead, on_delete=models.PROTECT, blank=True, null=True, related_name='head_duplicaes')
    discovered_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)