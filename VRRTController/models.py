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

    PatientID = models.CharField(default='VA_00_00', max_length=8) 
    
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

    # Resperation rate at start
    RespirationRateStart = models.PositiveIntegerField(default=0, help_text='Resperation rate at the start of session')

    # Resperation rate at end
    RespirationRateEnd = models.PositiveIntegerField(default=0, help_text='Resperation rate at the end of session')

    # Checkboxes
    RestlessnessStart = models.BooleanField(blank=True, default=False)
    RestlessnessEnd = models.BooleanField(blank=True, default=False)

    DepressionStart = models.BooleanField(blank=True, default=False)
    DepressionEnd = models.BooleanField(blank=True, default=False)

    NauseaStart = models.BooleanField(blank=True, default=False)
    NauseaEnd = models.BooleanField(blank=True, default=False)

    MobilityStart = models.BooleanField(blank=True, default=False)
    MobilityEnd = models.BooleanField(blank=True, default=False)

    AnxietyStart = models.BooleanField(blank=True, default=False)
    AnxietyEnd = models.BooleanField(blank=True, default=False)

    VisiblePainStart = models.BooleanField(blank=True, default=False)
    VisiblePainEnd = models.BooleanField(blank=True, default=False)

    TremorsStart = models.BooleanField(blank=True, default=False)
    TremorsEnd = models.BooleanField(blank=True, default=False)

    DelusionsStart = models.BooleanField(blank=True, default=False)
    DelusionsEnd = models.BooleanField(blank=True, default=False)

    # duration of therapy
    TherapyDuration = models.PositiveIntegerField(default=0, help_text='Length of therapy in minutes')

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


