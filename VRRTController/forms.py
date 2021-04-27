from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from .models import SiteID

User = get_user_model()
users = User.objects.filter(groups__name='Patient')

patients = []

for i in range(len(users)):
    patients.append((str(users[i]),str(users[i])))

patients.append(('All Patients', 'All Patients'))

# sitesIds = SiteID.objects.all().values_list('SiteName')

# sites = []

# for i in range(len(sitesIds)):
#     buffer = str(i) + str(sitesIds[i])
#     buffer = buffer.replace('\'','')
#     buffer = buffer.replace(',','')
#     sites.append(buffer)

sites = [
    ('1', 'Reno, NV'),
    ('2', 'Las Vegas, NV'),
    ('3', 'All Sites'),
]

datatypes = [
    ('1', 'Pain Score'),
    ('2', 'Heart Rate'),
    ('3', 'Blood Pressure'),
    ('4', 'Respiration Rate'),
    ('5', 'Oxygen Saturation'),
    ('1', 'All Data'),
]


class AnalysisSelectionForm(forms.Form):

    select_patient = forms.ChoiceField(choices = patients, label = "Patient")
    select_site = forms.ChoiceField(choices = sites, label = "Site")
    select_datatype = forms.ChoiceField(choices = datatypes, label = "DataType")

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
