from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from VRRTController.models import Survey, SurveyInstance, SiteID
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Legend, LegendItem
from django.contrib.auth import get_user_model
from django.http import QueryDict
import json
import sqlite3
from .forms import SignUpForm

from .forms import AnalysisSelectionForm
from django import forms

from django.contrib.auth.models import User, Group
"""
************************ METHODS ************************
"""

"""
pageUserAuth(request,neededGroup,pageTemplate,context=None)

The page User Auth function takes 4 paramaters
-request(pass in the request from the view function this is being called from)
-neededGroup is a string that is the name of the group the user needs to be in to access the current page Ex: neeededGroup = 'Staff'
-pageTemplate is a string that is the html file for the page that will be loaded if the user is apart of the correct group
-context This is a arr and is set to none by dafult and is not needed, only used in views where we are retreving data such as survey list

"""

def pageUserAuth(request,neededGroup,pageTemplate,context=None):

    userGroup = request.user.groups.filter(user=request.user)[0]
    userGroup = str(userGroup)
    #print("PageUserAuth: context: " + str(context))
    print("PageUserAuth: userGroup: " + str(userGroup))
    print("PageUserAuth: pageTemplate: " + str(pageTemplate))

    if context == None:
        print("PageUserAuth: context is empty")
        if userGroup == neededGroup:
            print("PageUserAuth: Group Check Passed")
            return render(request,pageTemplate)
        elif userGroup == 'Staff':
            print("PageUserAuth: Group Check Failed")
            return HttpResponseRedirect(reverse_lazy('staffLandingPage'))
        elif userGroup == 'Patient':
            print("PageUserAuth: Group Check Failed")
            return HttpResponseRedirect(reverse_lazy('patientLandingPage'))
        else:
            return HttpResponseRedirect(reverse_lazy('logout'))
    elif context != None:
        print("PageUserAuth: context is NOT empty")
        if userGroup == neededGroup:
            print("PageUserAuth: Group Check Passed")
            return render(request,pageTemplate,context)
        elif userGroup == 'Staff':
            print("PageUserAuth: Group Check Failed")
            return HttpResponseRedirect(reverse_lazy('staffLandingPage'))
        elif userGroup == 'Patient':
            print("PageUserAuth: Group Check Failed")
            return HttpResponseRedirect(reverse_lazy('patientLandingPage'))
        else:
            return HttpResponseRedirect(reverse_lazy('logout'))


"""
A function that takes in a string 
-Heartrate
-pain score
-BP
-BR
-O2Sat

Querrys the database of values for all the start and stops values
"""
def databaseQuery(field):

    results = []

    print("DATABASEQUERY CALLED")
    if field == 'painScore':
        startValues = SurveyInstance.objects.values_list('PainScoreStart')
        endValues = SurveyInstance.objects.values_list('PainScoreEnd')
    elif field == 'heartRate':
        startValues = SurveyInstance.objects.values_list('HeartRateStart')
        endValues = SurveyInstance.objects.values_list('HeartRateEnd')
    
    #Blood pressure is handled differently because its two values for every one instance
    elif field == 'bloodPressure':
        startValuesBP1 = SurveyInstance.objects.values_list('BPStartValue1')
        endValuesBP1 = SurveyInstance.objects.values_list('BPEndValue1')

        startValuesBP2 = SurveyInstance.objects.values_list('BPStartValue2')
        endValuesBP2 = SurveyInstance.objects.values_list('BPEndValue2')

        BP1Vals = []
        BP1Vals.append(startValuesBP1)
        BP1Vals.append(endValuesBP1)

        BP2Vals = []
        BP2Vals.append(startValuesBP2)
        BP2Vals.append(endValuesBP2)

        results.append(BP1Vals)
        results.append(BP2Vals)

        return results

    
    elif field == 'respirationRate':
        startValues = SurveyInstance.objects.values_list('RespirationRateStart')
        endValues = SurveyInstance.objects.values_list('RespirationRateEnd')

    elif field == 'O2Saturation':
        startValues = SurveyInstance.objects.values_list('PainScoreStart')
        endValues = SurveyInstance.objects.values_list('PainScoreEnd')

    startValues = list(startValues)
    endValues = list(endValues)

    #print(field + " start: " + str(startValues))
    #print(field + " start: type: " + str(type(startValues)))
    #print(field + " end: type: " + str(type(endValues)))
    print(field + " end: " + str(endValues))

    print("DATABASEQUERY: start list size: " + str(len(startValues)) + " end list size: " + str(len(endValues)))  

    
    results.append(startValues)
    results.append(endValues)
    return results



"""
This function takes in the array produced by databaseQuery and parses the data
returning it cleaned
"""

def databaseQuerryParser(values,field):

    results = []

    #Special handler for blood pressure
    if field == 'bloodPressure':
        startValues1 = []
        endValues1 = []

        startValues2 = []
        endValues2 = []

        for i in range(len(values[0][0])):
            startValues1.append(values[0][0][i][0])
            endValues1.append(values[0][1][i][0])
        for i in range(len(values[1][0])):
            startValues2.append(values[1][0][i][0])
            endValues2.append(values[1][1][i][0])
        
        BP1Vals  = []
        BP2Vals = []

        BP1Vals.append(startValues1)
        BP1Vals.append(endValues1)

        BP2Vals.append(startValues2)
        BP2Vals.append(endValues2)

        results.append(BP1Vals)
        results.append(BP2Vals)

        return results



    startValues = []
    endValues = []

    print("The size of values is: " + str(len(values)))

    for value in values[0]:
        startValues.append(value[0])
    
    for value in values[1]:
        endValues.append(value[0])

    print("Starting values: " + str(startValues))
    print("Ending values: " + str(endValues))

    

    results.append(startValues)
    results.append(endValues)

    return results
    


#Takes in the field (heart rate, pain score, etc) and userName is the current users name
def databaseUserQuery(field, userName):
    print("DATABASEQUERY CALLED")
    print("RETREAVING: " + str(field) + " FOR USER: " + str(userName))
    if field == 'painScore':
        startValues = SurveyInstance.objects.values_list('PainScoreStart').filter(PatientID = userName)
        #startValues = SurveyInstance.objects.filter(PatientID = userName,'PainScoreStart')
        endValues = SurveyInstance.objects.values_list('PainScoreEnd').filter(PatientID = userName)
    elif field == 'heartRate':
        startValues = SurveyInstance.objects.values_list('HeartRateStart').filter(PatientID = userName)
        endValues = SurveyInstance.objects.values_list('HeartRateEnd').filter(PatientID = userName)
    
    elif field == 'bloodPressure':
        startValuesBP1 = SurveyInstance.objects.values_list('BPStartValue1').filter(PatientID = userName)
        endValuesBP1 = SurveyInstance.objects.values_list('BPEndValue1').filter(PatientID = userName)

        startValuesBP2 = SurveyInstance.objects.values_list('BPStartValue1').filter(PatientID = userName)
        endValuesBP2 = SurveyInstance.objects.values_list('BPEndValue1').filter(PatientID = userName)
    
    elif field == 'respirationRate':
        startValues = SurveyInstance.objects.values_list('RespirationRateStart').filter(PatientID = userName)
        endValues = SurveyInstance.objects.values_list('RespirationRateEnd').filter(PatientID = userName)

    elif field == 'O2Saturation':
        startValues = SurveyInstance.objects.values_list('PainScoreStart').filter(PatientID = userName)
        endValues = SurveyInstance.objects.values_list('PainScoreEnd').filter(PatientID = userName)

    startValues = list(startValues)
    endValues = list(endValues)

    print(field + " start: " + str(startValues))
    #print(field + " start: type: " + str(type(startValues)))
    #print(field + " end: type: " + str(type(endValues)))
    print(field + " end: " + str(endValues))

    print("DATABASEQUERY: start list size: " + str(len(startValues)) + " end list size: " + str(len(endValues)))  

    results = []
    results.append(startValues)
    results.append(endValues)
    return results

"""
Average Change calculation fuction that calculates the average change between sets
"""
def averageChageCalculation(values):

    differinces = []

    print("The size of values is: " + str(len(values)))

    for position in range(len(values[0])):
        differinces.append(values[0][position]-values[1][position])


    sum = 0
    for value in differinces:
        sum += value
    
    if len(differinces) != 0:
        averageChange = sum/len(differinces)
    else:
        averageChange = 0

    averageChange = round(averageChange,2)

    if averageChange == 0:
        return "The average change is 0"
    elif averageChange > 0:
        return "The average change was a decrease of " + str(averageChange)
    elif averageChange < 0:
        averageChange = averageChange * -1
        return "The average change was a increase of " + str(averageChange)

    return averageChange


def maxPostiveChange(values):

    currentMax = 0

    for position in range(len(values[0])):
        buffer = values[0][position]-values[1][position]
        if buffer > currentMax:
            currentMax = buffer

    return currentMax


def minChange(values):

    currentMin = 1000

    for position in range(len(values[0])):
        buffer = values[0][position]-values[1][position]
        if buffer < currentMin:
            currentMin = buffer
    
    return currentMin

"""
Returns a int that is a count of painscore changes > 2
"""
def significantPainScoreChange(values):

    numSignificantChanges = 0

    for i in range(len(values[0])):
        if(values[0][i]-values[1][i]) >= 2:
            numSignificantChanges += 1

    return numSignificantChanges





""" 

************************ NON LOGIN VIEWS ************************

"""



def index(request):
    """View function for home page of site"""

    #Generate count fo rthe number of active sites
    num_Sites = SiteID.objects.all().count()

    #Generate counts for number of survey types
    num_Surveys = Survey.objects.all().count()

    #Generate counts of number of surveys taken
    num_Surveys_Submitted = SurveyInstance.objects.all().count()

    context = {
        'num_Sites': num_Sites,
        'num_Surveys': num_Surveys,
        'num_Surveys_Submitted':num_Surveys_Submitted,
    }

    return render(request,"patient_landing_page.html",context=context)


@login_required
def logInRedirect(request):
    group = request.user.groups.filter(user=request.user)[0]
    print(group.name)
    if group.name=="Staff":
        return HttpResponseRedirect(reverse_lazy('staffLandingPage'))
    elif group.name=="Patient":
        return HttpResponseRedirect(reverse_lazy('patientLandingPage'))

    context = {}
    template = "base_generic.html"
    return HttpResponseRedirect(reverse_lazy('index'))
    


class MissionStatmentView(generic.View):
    def get(self, request):
        return render(request, "mission_statment.html")

class SiteListView(generic.ListView):
    model = SiteID

def home_view(request):
    return render(request, 'admin_landing_pg.html')





""" 

************************ STAFF VIEWS ************************

"""

class staffLandingPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        userGRoup = request.user.groups.filter(user=request.user)[0]

        return pageUserAuth(request,'Staff',"admin_landing_pg.html")

class adminProgressResultsPage(LoginRequiredMixin, generic.View):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        userGRoup = request.user.groups.filter(user=request.user)[0]

        return pageUserAuth(request,'Staff',"admin_progress_results.html")
        
class adminProgressPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        if request.method == 'POST':
            form = AnalysisSelectionForm(request.POST)
            
            if form.is_valid():
                return HttpResponseRedirect('/thanks/')
        else:
            form = AnalysisSelectionForm()
        # #Get the user stuff
        # User = get_user_model()
        # #Get the list of patients
        # users = User.objects.filter(groups__name = "Patient")

        # #making an empty list that records the patients
        # patientList = []

        # #Step through the list of patients
        # for i in range(len(users)):
        #     #Append just the patient name to the the patientsList
        #     patientList.append(str(users[i]))

        # print("USERS: " + str(patientList))

        # return pageUserAuth(request,'Staff',"admin_progress.html")

        return render(request, "admin_progress.html", {'form': form})
        return pageUserAuth(request,'Staff',"admin_progress.html")
    def post(self,request):
        
        if request.method == 'POST':
            form = AnalysisSelectionForm(request.POST)
            #print("The fourm data type is: " + str(type(request.POST)))
            #print("Thr fourm is: " + str((form)))
            buffer = request.POST

            dropDownVal = list(buffer.values())[3]
            patientVal = form.data.get('select_patient')
            siteVal = list(buffer.values())[1]

            print("dropDownVal: |" + dropDownVal + "| patientVal: " + str(patientVal) + " siteVal: " + siteVal)
            
            if patientVal == 'All Patients':
                if dropDownVal == 'Pain Score':
                    return HttpResponseRedirect(reverse_lazy('adminPainScoreProgressView'))
                elif dropDownVal == 'Heart Rate':
                    return HttpResponseRedirect(reverse_lazy('adminHearRateProgressView'))
                elif dropDownVal == 'Blood Pressure':
                    return HttpResponseRedirect(reverse_lazy('adminBloodPressureProgressView'))
                elif dropDownVal == 'Resperation Rate':
                    return HttpResponseRedirect(reverse_lazy('adminResperationRateProgressView'))
                elif dropDownVal == 'Oxygen Saturation':
                    return HttpResponseRedirect(reverse_lazy('adminO2SaturationProgressView'))

            else:
                if dropDownVal == 'Pain Score':
                    return staffUserReview(patientVal,dropDownVal,request)
                elif dropDownVal == 'Heart Rate':
                    return staffUserReview(patientVal,dropDownVal,request)
                elif dropDownVal == 'Blood Pressure':
                    return staffUserReview(patientVal,dropDownVal,request)
                elif dropDownVal == 'Respiration Rate':
                    return staffUserReview(patientVal,dropDownVal,request)
                elif dropDownVal == 'Oxygen Saturation':
                    return staffUserReview(patientVal,dropDownVal,request)

            if form.is_valid():
                print("Fourm is valid ")
                
        else:
            form = AnalysisSelectionForm()

def staffUserReview(patientID,field,request):

        if field == "Pain Score":
            fieldValue = 'painScore'
        elif field == 'Heart Rate':
            fieldValue = 'heartRate'
        elif field == 'Blood Pressure':
            fieldValue = 'bloodPressure'
            fieldValue = 'bloodPressure'
            bloodPressure = True

            results = databaseQuery(fieldValue)

            results = databaseQuerryParser(results, fieldValue)

            print(results[0])

            systolicStartAvgChange = averageChageCalculation(list(results[0]))

            diastolicStartAvgChange = averageChageCalculation(list(results[1]))

            #Graph Stuff
            startValuesSystolic = results[0][0]
            endValuesSystolic = results[0][1]

            startValuesDiastolic = results[1][0]
            endValuesDiastolic = results[1][1]

            xVals = []

            for i in range(1,len(startValuesSystolic)+1):
                xVals.append(i)

            # source = ColumnDataSource(data=dict(
            #     x = xVals,
            #     y1 = startValues,
            #     y2 = endValues
            # ))

            p = figure( sizing_mode = "stretch_width", plot_height = 350)
            r = p.multi_line([xVals,xVals,xVals,xVals],[startValuesSystolic,endValuesSystolic,startValuesDiastolic,endValuesDiastolic], color=["firebrick", "firebrick","blue","blue"], alpha=[1, 0.3,1, 0.3], line_width=4)

            p.background_fill_color = None
            p.border_fill_color = None

            p.yaxis.axis_label = "Pain Score"
            p.xaxis.axis_label = "Session"

            legend = Legend(items=[
                LegendItem(label="Systolic Start Values", renderers=[r],  index=0),
                LegendItem(label="Systolic End Values", renderers=[r], index=1),
                LegendItem(label="Diastolic Start Values", renderers=[r],  index=2),
                LegendItem(label="Diastolic End Values", renderers=[r], index=3),
                ])
            p.add_layout(legend)

            p.legend.location = "top_left"
            p.legend.title_text_font = 'Arial'
            p.legend.title_text_font_size = '20pt'

            script, div = components(p)



            context = { 'bloodPressure' : bloodPressure, 'systolicStartAvgChange' : systolicStartAvgChange,
                        'diastolicStartAvgChange' : diastolicStartAvgChange,
                        'script' : script , 'div': div}
            return pageUserAuth(request,'Staff',"admin_progress_preview.html", context )
        elif field == 'Respiration Rate':
            fieldValue = 'respirationRate'
        elif field == 'Oxygen Saturation':
            fieldValue = 'O2Saturation'
        


        #fieldValue = field

        userName = patientID
        

        results = databaseUserQuery(fieldValue, userName)

        results = databaseQuerryParser(results,fieldValue)


        #Calculations
        averageChange = averageChageCalculation(results)
        maxPostiveChangeVal = maxPostiveChange(results)
        minChangeVal = minChange(results)
        if fieldValue == 'painScore':
            numOfSignificantChange = significantPainScoreChange(results)

        print("\t\tRESULTS: " + str(results))

        startValues = []
        endValues = []

        startValues = results[0]
        endValues = results[1]

        xVals = []

        for i in range(1,len(startValues)+1):
            xVals.append(i)

        #xVals = range(len(startValues))

        source = ColumnDataSource(data=dict(
            x = xVals,
            y1 = startValues,
            y2 = endValues
        ))

        p = figure( sizing_mode = "stretch_width", plot_height = 350)
        p.title = 'Change in Heart Rate'

        r = p.multi_line([xVals,xVals],[startValues,endValues], color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)

        p.background_fill_color = None
        p.border_fill_color = None

        p.yaxis.axis_label = "Heart Rate(BPM)"
        p.xaxis.axis_label = "Session"

        legend = Legend(items=[
            LegendItem(label="Start Values", renderers=[r],  index=0),
            LegendItem(label="End Values", renderers=[r], index=1),
            ])
        p.add_layout(legend)

        p.legend.location = "top_left"
        p.legend.title_text_font = 'Arial'
        p.legend.title_text_font_size = '20pt'

        script, div = components(p)

        if fieldValue == 'painScore':
            context = { 'averageChange' : averageChange, 'maxPostiveChange' : maxPostiveChangeVal,
                        'minChange' : minChangeVal, 'significantChanges' : numOfSignificantChange,
                        'script' : script , 'div': div}
        elif field == 'Heart Rate':
            fieldValue = 'heartRate'
            context = { 'averageChange' : averageChange, 'maxPostiveChange' : maxPostiveChangeVal,
                    'minChange' : minChangeVal, 
                    'script' : script , 'div': div}
        elif field == 'Blood Pressure':
            fieldValue = 'bloodPressure'
            context = { 'bloodPressure' : bloodPressure, 'systolicStartAvgChange' : systolicStartAvgChange,
                    'diastolicStartAvgChange' : diastolicStartAvgChange,
                    'script' : script , 'div': div}
        elif field == 'Respiration Rate':
            fieldValue = 'respirationRate'
            context = { 'averageChange' : averageChange, 'maxPostiveChange' : maxPostiveChangeVal,
                     'minChange' : minChangeVal,
                     'script' : script , 'div': div}
        elif field == 'Oxygen Saturation':
            fieldValue = 'O2Saturation'
            context = { 'averageChange' : averageChange, 'maxPostiveChange' : maxPostiveChangeVal,
                     'minChange' : minChangeVal,
                     'script' : script , 'div': div}

       

        return pageUserAuth(request,'Staff',"admin_progress_preview.html", context )


class adminProgressPreviewPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        databaseEntrie = SurveyInstance.objects.all()

        #print(databaseEntrie)

        databaseEntriePainStart = SurveyInstance.objects.values_list('PainScoreStart')
        databaseEntriePainEnd = SurveyInstance.objects.values_list('PainScoreEnd')

        #print("Starting pain scores: " + str(databaseEntriePainStart))
        #print("Ending pain scores: " + str(databaseEntriePainEnd))



        



        return pageUserAuth(request,'Staff',"admin_progress_preview.html")

        return render(request, "admin_progress_preview.html")

class adminPainScoreProgressView(LoginRequiredMixin, generic.View):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        #Setting a variable for the current field name
        fieldValue = 'painScore'
        #Using databaseQuery to get the database instances off this object
        results = databaseQuery(fieldValue)
        #Turning the results into a list
        results = databaseQuerryParser(results, fieldValue)


        #Calculations
        averageChange = averageChageCalculation(results)
        maxPostiveChangeVal = maxPostiveChange(results)
        minChangeVal = minChange(results)
        numOfSignificantChange = significantPainScoreChange(results)


        #Graph Stuff
        startValues = results[0]
        endValues = results[1]

        xVals = []

        for i in range(1,len(startValues)+1):
            xVals.append(i)

        source = ColumnDataSource(data=dict(
            x = xVals,
            y1 = startValues,
            y2 = endValues
        ))

        p = figure( sizing_mode = "stretch_width", plot_height = 350)
        r = p.multi_line([xVals,xVals],[startValues,endValues], color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)

        p.background_fill_color = None
        p.border_fill_color = None

        p.yaxis.axis_label = "Pain Score"
        p.xaxis.axis_label = "Session"

        legend = Legend(items=[
            LegendItem(label="Start Values", renderers=[r],  index=0),
            LegendItem(label="End Values", renderers=[r], index=1),
            ])
        p.add_layout(legend)

        p.legend.location = "top_left"
        p.legend.title_text_font = 'Arial'
        p.legend.title_text_font_size = '20pt'


        script, div = components(p)


        #Dictionary of the variables to be passed to the webpage
        context = { 'averageChange' : averageChange, 'maxPostiveChange' : maxPostiveChangeVal,
                     'minChange' : minChangeVal, 'significantChanges' : numOfSignificantChange,
                     'script' : script , 'div': div}

        return pageUserAuth(request,'Staff',"admin_progress_preview.html",context)

class adminBloodPressureProgressView(LoginRequiredMixin, generic.View):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        fieldValue = 'bloodPressure'
        bloodPressure = True

        results = databaseQuery(fieldValue)

        results = databaseQuerryParser(results, fieldValue)

        print(results[0])

        systolicStartAvgChange = averageChageCalculation(list(results[0]))

        diastolicStartAvgChange = averageChageCalculation(list(results[1]))

        #Graph Stuff
        startValuesSystolic = results[0][0]
        endValuesSystolic = results[0][1]

        startValuesDiastolic = results[1][0]
        endValuesDiastolic = results[1][1]

        xVals = []

        for i in range(1,len(startValuesSystolic)+1):
            xVals.append(i)

        # source = ColumnDataSource(data=dict(
        #     x = xVals,
        #     y1 = startValues,
        #     y2 = endValues
        # ))

        p = figure( sizing_mode = "stretch_width", plot_height = 350)
        r = p.multi_line([xVals,xVals,xVals,xVals],[startValuesSystolic,endValuesSystolic,startValuesDiastolic,endValuesDiastolic], color=["firebrick", "firebrick","blue","blue"], alpha=[1, 0.3,1, 0.3], line_width=4)

        p.background_fill_color = None
        p.border_fill_color = None

        p.yaxis.axis_label = "Pain Score"
        p.xaxis.axis_label = "Session"

        legend = Legend(items=[
            LegendItem(label="Systolic Start Values", renderers=[r],  index=0),
            LegendItem(label="Systolic End Values", renderers=[r], index=1),
            LegendItem(label="Diastolic Start Values", renderers=[r],  index=2),
            LegendItem(label="Diastolic End Values", renderers=[r], index=3),
            ])
        p.add_layout(legend)

        p.legend.location = "top_left"
        p.legend.title_text_font = 'Arial'
        p.legend.title_text_font_size = '20pt'


        script, div = components(p)



        context = { 'bloodPressure' : bloodPressure, 'systolicStartAvgChange' : systolicStartAvgChange,
                    'diastolicStartAvgChange' : diastolicStartAvgChange,
                    'script' : script , 'div': div}

        

        return pageUserAuth(request,'Staff',"admin_progress_preview.html", context)
        

class adminHearRateProgressView(LoginRequiredMixin, generic.View):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        fieldValue = 'heartRate'
        #Setting a variable for the current field name
        #Using databaseQuery to get the database instances off this object
        results = databaseQuery(fieldValue)
        #Turning the results into a list
        results = databaseQuerryParser(results, fieldValue)


        #Calculations
        averageChange = averageChageCalculation(results)
        maxPostiveChangeVal = maxPostiveChange(results)
        minChangeVal = minChange(results)
        numOfSignificantChange = significantPainScoreChange(results)


        #Graph Stuff
        startValues = results[0]
        endValues = results[1]

        xVals = []

        for i in range(1,len(startValues)+1):
            xVals.append(i)

        #xVals = range(len(startValues))

        source = ColumnDataSource(data=dict(
            x = xVals,
            y1 = startValues,
            y2 = endValues
        ))

        p = figure( sizing_mode = "stretch_width", plot_height = 350)

        r = p.multi_line([xVals,xVals],[startValues,endValues], color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)

        p.background_fill_color = None
        p.border_fill_color = None

        p.yaxis.axis_label = "BPM"
        p.xaxis.axis_label = "Session"

        legend = Legend(items=[
            LegendItem(label="Start Values", renderers=[r],  index=0),
            LegendItem(label="End Values", renderers=[r], index=1),
            ])
        p.add_layout(legend)

        p.legend.location = "top_left"
        p.legend.title_text_font = 'Arial'
        p.legend.title_text_font_size = '20pt'

        script, div = components(p)


        #Dictionary of the variables to be passed to the webpage
        context = { 'averageChange' : averageChange, 'maxPostiveChange' : maxPostiveChangeVal,
                     'minChange' : minChangeVal,
                     'script' : script , 'div': div}

        return pageUserAuth(request,'Staff',"admin_progress_preview.html",context)

class adminResperationRateProgressView(LoginRequiredMixin, generic.View):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        fieldValue = 'respirationRate'
        #Using databaseQuery to get the database instances off this object
        results = databaseQuery(fieldValue)
        #Turning the results into a list
        results = databaseQuerryParser(results, fieldValue)


        #Calculations
        averageChange = averageChageCalculation(results)
        maxPostiveChangeVal = maxPostiveChange(results)
        minChangeVal = minChange(results)
        numOfSignificantChange = significantPainScoreChange(results)


        #Graph Stuff
        startValues = results[0]
        endValues = results[1]

        xVals = []

        for i in range(1,len(startValues)+1):
            xVals.append(i)

        #xVals = range(len(startValues))

        source = ColumnDataSource(data=dict(
            x = xVals,
            y1 = startValues,
            y2 = endValues
        ))

        p = figure( sizing_mode = "stretch_width", plot_height = 350)

        r = p.multi_line([xVals,xVals],[startValues,endValues], color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)

        p.background_fill_color = None
        p.border_fill_color = None

        p.yaxis.axis_label = "Resperation Rate(Breaths/m)"
        p.xaxis.axis_label = "Session"

        legend = Legend(items=[
            LegendItem(label="Start Values", renderers=[r],  index=0),
            LegendItem(label="End Values", renderers=[r], index=1),
            ])
        p.add_layout(legend)

        p.legend.location = "top_left"
        p.legend.title_text_font = 'Arial'
        p.legend.title_text_font_size = '20pt'

        script, div = components(p)


        #Dictionary of the variables to be passed to the webpage
        context = { 'averageChange' : averageChange, 'maxPostiveChange' : maxPostiveChangeVal,
                     'minChange' : minChangeVal,
                     'script' : script , 'div': div}

        return pageUserAuth(request,'Staff',"admin_progress_preview.html",context)

class adminO2SaturationProgressView(LoginRequiredMixin, generic.View):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        fieldValue = 'O2Saturation'
        #Using databaseQuery to get the database instances off this object
        results = databaseQuery(fieldValue)
        #Turning the results into a list
        results = databaseQuerryParser(results, fieldValue)


        #Calculations
        averageChange = averageChageCalculation(results)
        maxPostiveChangeVal = maxPostiveChange(results)
        minChangeVal = minChange(results)
        numOfSignificantChange = significantPainScoreChange(results)


        #Graph Stuff
        startValues = results[0]
        endValues = results[1]

        xVals = []

        for i in range(1,len(startValues)+1):
            xVals.append(i)

        #xVals = range(len(startValues))

        # source = ColumnDataSource(data=dict(
        #     x = xVals,
        #     y1 = startValues,
        #     y2 = endValues
        # ))

        legends = {'labels': ["Starting Values", "Ending Values"] }



        p = figure( sizing_mode = "stretch_width", plot_height = 350)

        r = p.multi_line([xVals,xVals],[startValues,endValues], color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)

        p.background_fill_color = None
        p.border_fill_color = None

        p.yaxis.axis_label = "Oxygen Saturation(%)"
        p.xaxis.axis_label = "Session"

        legend = Legend(items=[
            LegendItem(label="Start Values", renderers=[r],  index=0),
            LegendItem(label="End Values", renderers=[r], index=1),
            ])
        p.add_layout(legend)

        p.legend.location = "top_left"
        p.legend.title_text_font = 'Arial'
        p.legend.title_text_font_size = '20pt'

        script, div = components(p)


        #Dictionary of the variables to be passed to the webpage
        context = { 'averageChange' : averageChange, 'maxPostiveChange' : maxPostiveChangeVal,
                     'minChange' : minChangeVal,
                     'script' : script , 'div': div}

        return pageUserAuth(request,'Staff',"admin_progress_preview.html",context)

class surveyInputPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        return pageUserAuth(request,'Staff',"survey_input.html")

        return render(request, "survey_input.html")

class surveyVerifyPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        return pageUserAuth(request,'Staff',"survey_verify.html")

        return render(request, "survey_verify.html")


import csv 

from django.shortcuts import render
from django.http import HttpResponse
from .models import SurveyInstance

def export(request):


    usersGroup = request.user.groups.filter(user=request.user)[0]

    if usersGroup.name == "Staff":
        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response)
        writer.writerow(['Survey ID','Patient ID','Pain Score Start','Pain Score End'
                    ,'Heart Rate Start','Heart Rate End', 'Starting Systolic', 'Starting Diastolic'
                    ,'End Systolic', 'End Diastolic','O2 Saturation Start','O2 Saturation End'
                    ,'Resperation Start','Resperation End'])

        for row in SurveyInstance.objects.all().values_list('id','PatientID','PainScoreStart','PainScoreEnd','HeartRateStart','HeartRateEnd','BPStartValue1','BPStartValue2',
                                                            'BPEndValue1','BPEndValue2','O2SaturationStart','O2SaturationEnd','RespirationRateStart','RespirationRateEnd'):
            writer.writerow(row)

        response['Content-Disposition'] = 'attachment; filename="SurveyResponses.csv'

        return response
    return reverse_lazy('login')

import os
def exportChat(request):
    usersGroup = request.user.groups.filter(user=request.user)[0]

    

    if usersGroup.name == "Staff":            
        response = HttpResponse(content_type='text/csv')

        connection = sqlite3.connect("bert//actions//rasa.db")
    
        csvWriter = csv.writer(response)
        c = connection.cursor()

        csvWriter.writerow(["Pain","Pain Location","Missed Events","Sleep","Stress","VR Feedback"])

        c.execute("select * from slots")

        rows = c.fetchall()

        print("Rows: " + str(rows))

        for x in rows:
            print("Writing row: " + str(x))
            csvWriter.writerow(x)

        response['Content-Disposition'] = 'attachment; filename="ChatData.csv'

        return response
    return reverse_lazy('login')
        



class accountCreationSelection(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        return pageUserAuth(request,'Staff',"admin_create_new_selection.html")

def createPatient(request):

    usersGroup = request.user.groups.filter(user=request.user)[0]

    if usersGroup.name == "Staff":
        form = SignUpForm(request.POST)
        if form.is_valid(): 

            form.save()
            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password1')

            #email = form.cleaned_data.get('email')

            user = authenticate(username=username, password=password)

            user.save()

            user_group = Group.objects.get(name='Patient') 

            user.groups.add(user_group)

            
            
            return render(request, 'admin_landing_pg.html')
        return render(request, 'admin_create_new_patient.html', {'form':form})
        
def createStaff(request):

    usersGroup = request.user.groups.filter(user=request.user)[0]

    if usersGroup.name == "Staff":
        form = SignUpForm(request.POST)
        if form.is_valid(): 

            form.save()
            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)

            user.save()

            user_group = Group.objects.get(name='Staff') 

            user.groups.add(user_group)

            
            return pageUserAuth(request,'Staff',"admin_landing_pg.html")

        return pageUserAuth(request,'Staff',"admin_create_new_staff.html", {'form':form})

"""
    These two functions are from before and need to be updated
"""

class SurveyInstanceListView(generic.ListView):
    model = SurveyInstance 
    
class SurveyCreate(CreateView):
    model = SurveyInstance
    fields = ['PainScoreStart','PainScoreEnd', 'HeartRateStart', 
        'HeartRateEnd', 'BPStartValue1', 'BPStartValue2', 
        'BPEndValue1', 'BPEndValue2', 'RespirationRateStart', 'RespirationRateEnd', 'O2SaturationStart',
        'O2SaturationEnd', 'RestlessnessStart', 'RestlessnessEnd', 'DepressionStart', 'DepressionEnd', 
        'NauseaStart', 'NauseaEnd', 'MobilityStart', 'MobilityEnd', 'AnxietyStart', 'AnxietyEnd', 
        'VisiblePainStart', 'VisiblePainEnd', 'TremorsStart', 'TremorsEnd', 'DelusionsStart', 
        'DelusionsEnd','TherapyDuration', 'PatientID']
    success_url = reverse_lazy('staffLandingPage')

def showthis(request):
    
    count= SurveyInstance.objects.all().count()
    
    context= {'count': count}

    def get(self, request):
        return render(request, 'patient_landing_page.html', context)

""" 

************************ PATIENT VIEWS ************************

"""

class patientLandingPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        userName = ""
        #Checks if the current uesr has been authed
        if request.user.is_authenticated:
            #Getting the current users username
            userName = request.user.username

        #Getting all of the survey instances where the patient ID matches 
        # the current users username
        SurveyInstances = SurveyInstance.objects.filter(PatientID = userName)

        #Getting the count of them
        numSurveys = len(SurveyInstances)

        print("\t\tUSER: " + str(userName) + " has submited " + str(numSurveys) + " surveys" )

        #Creating the variable that will be passed to the webpage
        context = {'num_Surveys' : numSurveys}

        #Passing the context dictionary to the return function
        return pageUserAuth(request,'Patient',"patient_landing_page.html",context)
       
        return render(request, "patient_landing_page.html")
   

class patientProgressPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        userName = ""
        #Checks if the current uesr has been authed
        if request.user.is_authenticated:
            #Getting the current users username
            userName = request.user.username

        databaseUserQuery("painScore", userName)

        # graph x, y coordinates
        x = [ 1, 2, 3, 4, 5 ]
        y = [ 1, 2, 3, 4, 5 ]

        #setup graph plot
        plot = figure(title= 'Line Graph', x_axis_label= 'X-Axis', y_axis_label= 'Y-Axis', sizing_mode = "stretch_width", plot_height = 350)

        #plot line
        plot.line( x, y, line_width=2 )
        plot.background_fill_color = None
        plot.border_fill_color = None
        #store components
        script, div = components(plot)
        return pageUserAuth(request,'Patient',"patient_progress.html", {'script' : script , 'div': div} )

class patientProgressPagePainScore(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        fieldValue = "painScore"

        userName = ""
        #Checks if the current uesr has been authed
        if request.user.is_authenticated:
            #Getting the current users username
            userName = request.user.username

        results = databaseUserQuery(fieldValue, userName)

        results = databaseQuerryParser(results,fieldValue)

        print("\t\tRESULTS: " + str(results))

        startValues = results[0]
        endValues = results[1]

        xVals = []

        for i in range(1,len(startValues)+1):
            xVals.append(i)

        #xVals = range(len(startValues))

        source = ColumnDataSource(data=dict(
            x = xVals,
            y1 = startValues,
            y2 = endValues
        ))

        p = figure( sizing_mode = "stretch_width", plot_height = 350)
        p.title = 'Change in Pain Score'

        r = p.multi_line([xVals,xVals],[startValues,endValues], color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)

        p.background_fill_color = None
        p.border_fill_color = None

        p.yaxis.axis_label = "Pain Score"
        p.xaxis.axis_label = "Session"

        legend = Legend(items=[
            LegendItem(label="Start Values", renderers=[r],  index=0),
            LegendItem(label="End Values", renderers=[r], index=1),
            ])
        p.add_layout(legend)

        p.legend.location = "top_left"
        p.legend.title_text_font = 'Arial'
        p.legend.title_text_font_size = '20pt'

        script, div = components(p)

        return pageUserAuth(request,'Patient',"patient_progress.html", {'script' : script , 'div': div} )

class patientProgressBloodPressure(LoginRequiredMixin, generic.View):

    def get(self, request):
        fieldValue = 'bloodPressure'
        bloodPressure = True

        results = databaseQuery(fieldValue)

        results = databaseQuerryParser(results, fieldValue)

        print(results[0])

        systolicStartAvgChange = averageChageCalculation(list(results[0]))

        diastolicStartAvgChange = averageChageCalculation(list(results[1]))

        #Graph Stuff
        startValuesSystolic = results[0][0]
        endValuesSystolic = results[0][1]

        startValuesDiastolic = results[1][0]
        endValuesDiastolic = results[1][1]

        xVals = []

        for i in range(1,len(startValuesSystolic)+1):
            xVals.append(i)

        # source = ColumnDataSource(data=dict(
        #     x = xVals,
        #     y1 = startValues,
        #     y2 = endValues
        # ))

        p = figure( sizing_mode = "stretch_width", plot_height = 350)
        r = p.multi_line([xVals,xVals,xVals,xVals],[startValuesSystolic,endValuesSystolic,startValuesDiastolic,endValuesDiastolic], color=["firebrick", "firebrick","blue","blue"], alpha=[1, 0.3,1, 0.3], line_width=4)

        p.background_fill_color = None
        p.border_fill_color = None

        p.yaxis.axis_label = "Pain Score"
        p.xaxis.axis_label = "Session"

        legend = Legend(items=[
            LegendItem(label="Systolic Start Values", renderers=[r],  index=0),
            LegendItem(label="Systolic End Values", renderers=[r], index=1),
            LegendItem(label="Diastolic Start Values", renderers=[r],  index=2),
            LegendItem(label="Diastolic End Values", renderers=[r], index=3),
            ])
        p.add_layout(legend)

        p.legend.location = "top_left"
        p.legend.title_text_font = 'Arial'
        p.legend.title_text_font_size = '20pt'

        script, div = components(p)



        context = { 'bloodPressure' : bloodPressure, 'systolicStartAvgChange' : systolicStartAvgChange,
                    'diastolicStartAvgChange' : diastolicStartAvgChange,
                    'script' : script , 'div': div}

        

        return pageUserAuth(request,'Patient',"patient_progress.html", context)


class patientProgressPageHeartRate(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        fieldValue = "heartRate"

        userName = ""
        #Checks if the current uesr has been authed
        if request.user.is_authenticated:
            #Getting the current users username
            userName = request.user.username

        results = databaseUserQuery(fieldValue, userName)

        results = databaseQuerryParser(results,fieldValue)

        print("\t\tRESULTS: " + str(results))

        startValues = results[0]
        endValues = results[1]

        xVals = []

        for i in range(1,len(startValues)+1):
            xVals.append(i)

        #xVals = range(len(startValues))

        source = ColumnDataSource(data=dict(
            x = xVals,
            y1 = startValues,
            y2 = endValues
        ))

        p = figure( sizing_mode = "stretch_width", plot_height = 350)
        p.title = 'Change in Heart Rate'

        r = p.multi_line([xVals,xVals],[startValues,endValues], color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)

        p.background_fill_color = None
        p.border_fill_color = None

        p.yaxis.axis_label = "Heart Rate(BPM)"
        p.xaxis.axis_label = "Session"

        legend = Legend(items=[
            LegendItem(label="Start Values", renderers=[r],  index=0),
            LegendItem(label="End Values", renderers=[r], index=1),
            ])
        p.add_layout(legend)

        p.legend.location = "top_left"
        p.legend.title_text_font = 'Arial'
        p.legend.title_text_font_size = '20pt'

        script, div = components(p)

        return pageUserAuth(request,'Patient',"patient_progress.html", {'script' : script , 'div': div} )

class patientProgressPageOxygenSaturation(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        fieldValue = "O2Saturation"

        userName = ""
        #Checks if the current uesr has been authed
        if request.user.is_authenticated:
            #Getting the current users username
            userName = request.user.username

        results = databaseUserQuery(fieldValue, userName)

        results = databaseQuerryParser(results,fieldValue)

        print("\t\tRESULTS: " + str(results))

        startValues = results[0]
        endValues = results[1]

        xVals = []

        for i in range(1,len(startValues)+1):
            xVals.append(i)

        #xVals = range(len(startValues))

        source = ColumnDataSource(data=dict(
            x = xVals,
            y1 = startValues,
            y2 = endValues
        ))

        p = figure( sizing_mode = "stretch_width", plot_height = 350)

        r = p.multi_line([xVals,xVals],[startValues,endValues], color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)

        p.background_fill_color = None
        p.border_fill_color = None
        p.title = 'Change in Oxygen Saturation'

        p.yaxis.axis_label = "Oxygen Saturation(%)"
        p.xaxis.axis_label = "Session"

        legend = Legend(items=[
            LegendItem(label="Start Values", renderers=[r],  index=0),
            LegendItem(label="End Values", renderers=[r], index=1),
            ])
        p.add_layout(legend)

        p.legend.location = "top_left"
        p.legend.title_text_font = 'Arial'
        p.legend.title_text_font_size = '20pt'

        script, div = components(p)

        return pageUserAuth(request,'Patient',"patient_progress.html", {'script' : script , 'div': div} )

class patientProgressPageRespirationRate(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        fieldValue = "respirationRate"

        userName = ""
        #Checks if the current uesr has been authed
        if request.user.is_authenticated:
            #Getting the current users username
            userName = request.user.username

        results = databaseUserQuery(fieldValue, userName)

        results = databaseQuerryParser(results,fieldValue)

        print("\t\tRESULTS: " + str(results))

        startValues = results[0]
        endValues = results[1]

        xVals = []

        for i in range(1,len(startValues)+1):
            xVals.append(i)

        #xVals = range(len(startValues))

        source = ColumnDataSource(data=dict(
            x = xVals,
            y1 = startValues,
            y2 = endValues
        ))

        p = figure( sizing_mode = "stretch_width", plot_height = 350)

        r = p.multi_line([xVals,xVals],[startValues,endValues], color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)

        p.background_fill_color = None
        p.border_fill_color = None
        p.title = 'Change in Respiration Rate'

        p.yaxis.axis_label = "RespirationRate(Breaths/m)"
        p.xaxis.axis_label = "Session"

        legend = Legend(items=[
            LegendItem(label="Start Values", renderers=[r],  index=0),
            LegendItem(label="End Values", renderers=[r], index=1),
            ])
        p.add_layout(legend)

        p.legend.location = "top_left"
        p.legend.title_text_font = 'Arial'
        p.legend.title_text_font_size = '20pt'

        script, div = components(p)

        return pageUserAuth(request,'Patient',"patient_progress.html", {'script' : script , 'div': div} )

class chatbotPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        return pageUserAuth(request,'Patient',"chatbot.html")

        return render(request, "chatbot.html")




