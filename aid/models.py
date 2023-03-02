from django.db import models
from django.urls import reverse
# from account.models import Stuff

# Create your models here.
AID_CATEGORY = (
    ('Food Items', 'Food Items'),
    ('NFI', 'NFI'),
    ('Nutrients', 'Nutrients'),
    ('Hygiene', 'Hygiene'),
    ('Shelter', 'Shelter')
)
METRIC = (
    ('Kg.', 'Kg.'),
    ('Ltr.', 'Ltr.'),
    ('Qty.', 'Qty.')
)
ALLOCATION_SCHEME = (
    ('per family', 'per family'), 
    ('per person', 'per person'),
    ('per child', 'per child'),
    ('per lactating', 'per lactating'),
    ('per pregnant', 'per pregnant'),
    ('per disabled', 'per disabled'),
    ('per elderly', 'per elderly')
)

TARGET_GROUP = (
    (None, '-----------'),
    ('Family', 'Family'),
    ('Children', 'Children'),
    ('Pregnant or Lactating', 'Pregnant or Lactating'),
    ('Disabled', 'Disabled'),
    ('Elderly', 'Elderly')
)

class AidPackage(models.Model):
    package_name = models.CharField('Aid package name', max_length=100)
    target_group = models.CharField('Target Group', max_length = 30, choices = TARGET_GROUP, default='')
    quota = models.PositiveIntegerField(default=0)
    distribution_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)
    # created_by = models.ForeignKey(Stuff, related_name='packages', on_delete=models.CASCADE, null=True, default='')
    
    def __str__(self):
        return self.package_name

    def get_absolute_url(self):
        return reverse('aid:package_list')

    def aid_items(self):
        return AidItem.objects.filter(aid_package=self).count()

class AidItem(models.Model):
    name = models.CharField('Aid Name', max_length=30)
    category = models.CharField('Category', max_length = 30, choices = AID_CATEGORY)
    metric = models.CharField('Metric', max_length = 10, choices=METRIC)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    allocation_scheme = models.CharField('Allocation Scheme', max_length = 20, choices = ALLOCATION_SCHEME)
    aid_package = models.ForeignKey(AidPackage, related_name='items', on_delete=models.CASCADE)
    # created_by = models.ForeignKey(Stuff, related_name='aiditems', on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.name


