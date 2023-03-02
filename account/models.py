from django.db import models
from django.contrib.auth.models import User

# Create your models here.

JOB_ROLES = (
    ('Admin', 'Admin'),
    ('City Socio-Economic Office', 'City Socio-Economic Office'),
    ('Subcity Socio-Economic Office', 'Subcity Socio-Economic Office'),
)

SUB_CITIES = (
    ('Mekelle City Administration', 'Mekelle City Administration'),
    ('Adi Haqi', 'Adi Haqi'),
    ('Hawelti', 'Hawelti'),
    ('Hadinet', 'Hadinet'),
    ('Kedamay Woyane','Kedamay Woyane'),
    ('Semien', 'Semien'),
    ('Ayder', 'Ayder'),
    ('Quiha', 'Quiha')
)

class Stuff(models.Model):
    user = models.OneToOneField(User, related_name="stuff", blank=True, null=True, on_delete=models.PROTECT)
    role = models.CharField(max_length = 30, choices = JOB_ROLES)
    work_place = models.CharField(max_length = 30, choices = SUB_CITIES)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name