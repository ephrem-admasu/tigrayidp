from django import forms
from .models import AidPackage, AidItem

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
    ('per person', 'per person'),
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
    ('Pregnant', 'Pregnant'),
    ('Lactating', 'Lactating'),
    ('Disabled', 'Disabled'),
    ('Elderly', 'Elderly')
)

class DateInput(forms.DateInput):
    input_type = 'date'

class AidItemForm(forms.ModelForm):
   
    class Meta:
        model = AidItem
       
        verbose_name_plural = 'Aid Items'
        fields = '__all__'

class AidPackageForm(forms.ModelForm):
   
    class Meta:
        model = AidPackage
        widgets = {
            'distribution_date': DateInput(),
        }
       
        verbose_name_plural = 'Aid Packages'
        fields = '__all__'

