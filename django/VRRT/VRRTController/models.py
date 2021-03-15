from django.db import models
from django import forms

# Create your models here.


from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Survey(models.Model):
    """Survey model"""

    #Name of survey based on location
    SurveyName = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Model object."""
        return self.SurveyName
    
    # def get_absolute_url(self):
    #     """Returns the url to access a detail record for this book."""
    #     return reverse('book-detail', args=[str(self.id)])


import uuid #Required for unique survey instances

class SurveyInstance(models.Model):
    """Model reprsenting a specic instance of a survey"""

    #Survey object
    survey = models.ForeignKey('Survey',on_delete=models.SET_NULL, null=True)

    #ID for the specfic survey instance
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular survey')

    #Pain score at start of session
    PainScoreStart = models.PositiveIntegerField(default=0)

    #Pain score at end of session
    PainScoreEnd = models.PositiveIntegerField(default=0)

    # Heart rate at start of session
    HeartRateStart = models.PositiveIntegerField(default=0, help_text='Heart Rate at the start of session')

    # Heart rate at end of session
    HeartRateEnd = models.PositiveIntegerField(default=0, help_text='Heart Rate at the end of session')

    # Blood Pressure at start
    BPStartValue1 = models.PositiveIntegerField(default=0, help_text='Blood Pressure value1 at the start of session')
    BPStartValue2 = models.PositiveIntegerField(default=0, help_text='Blood Pressure value2 at the start of session')

    # Blood Pressure at end
    BPEndValue1 = models.PositiveIntegerField(default=0, help_text='Blood Pressure value1 at the end of session')
    BPEndValue2 = models.PositiveIntegerField(default=0, help_text='Blood Pressure value2 at the end of session')
    
    # O2 saturation at start
    O2SaturationStart = models.PositiveIntegerField(default=0, help_text='Oxygen saturation level at start of session')

    # O2 saturation at the end
    O2SaturationEnd = models.PositiveIntegerField(default=0, help_text='Oxygen saturation level at the end of session')


class SiteID(models.Model):
    """A model that describes the VA location"""

    SiteName = models.CharField(default='NOT SET', max_length=200, help_text='Enter the site location or name')

    SiteAddress = models.CharField(default='NOT SET', max_length=200, help_text='Enter the site street address')

    SiteState = models.CharField(default='NOT SET', max_length=200, help_text='Enter the site state')

    SiteCity = models.CharField(default='NOT SET', max_length=200, help_text='Enter the site city')

    SiteZipCode = models.CharField(default='NOT SET', max_length=200, help_text='Enther the site zip code')

    SiteTelephone = models.CharField(default='NOT SET', max_length=200, help_text='Enter the site telephone number')

    def __str__(self):
        """String that reprsents the model object."""

        return self.SiteName


