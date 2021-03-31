from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from VRRTController.models import Survey, SurveyInstance, SiteID
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import json


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
    print("PageUserAuth: context: " + str(context))
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
    print("DATABASEQUERY CALLED")
    if field == 'painScore':
        startValues = SurveyInstance.objects.values_list('PainScoreStart')
        endValues = SurveyInstance.objects.values_list('PainScoreEnd')
    elif field == 'heartRate':
        startValues = SurveyInstance.objects.values_list('HeartRateStart')
        endValues = SurveyInstance.objects.values_list('HeartRateEnd')
    
    elif field == 'bloodPressure':
        startValues = SurveyInstance.objects.values_list('PainScoreStart')
        endValues = SurveyInstance.objects.values_list('PainScoreEnd')
    
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

    results = []
    results.append(startValues)
    results.append(endValues)
    return results

"""
This function takes in the array produced by databaseQuery and parses the data
returning it cleaned
"""

def databaseQuerryParser(values,field):
    if field == 'bloodPressure':
        pass

    startValues = []
    endValues = []

    print("The size of values is: " + str(len(values)))

    for value in values[0]:
        startValues.append(value[0])
    
    for value in values[1]:
        endValues.append(value[0])

    print("Starting values: " + str(startValues))
    print("Ending values: " + str(endValues))

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
    
    averageChange = sum/len(differinces)

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

        return pageUserAuth(request,'Staff',"admin_progress.html")

        return render(request, "admin_progress.html")


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

        fieldValue = 'painScore'
        results = databaseQuery(fieldValue)

        results = databaseQuerryParser(results, fieldValue)

        averageChange = averageChageCalculation(results)

        maxPostiveChangeVal = maxPostiveChange(results)

        minChangeVal = minChange(results)


        context = { 'averageChange' : averageChange, 'maxPostiveChange' : maxPostiveChangeVal, 'minChange' : minChangeVal}

        return pageUserAuth(request,'Staff',"admin_progress_preview.html",context)
        

class adminHearRateProgressView(LoginRequiredMixin, generic.View):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        fieldValue = 'heartRate'
        results = databaseQuery(fieldValue)

        results = databaseQuerryParser(results, fieldValue)

        averageChange = averageChageCalculation(results)

        maxPostiveChangeVal = maxPostiveChange(results)

        minChangeVal = minChange(results)


        context = { 'averageChange' : averageChange, 'maxPostiveChange' : maxPostiveChangeVal, 'minChange' : minChangeVal}

        return pageUserAuth(request,'Staff',"admin_progress_preview.html",context)

class adminResperationRateProgressView(LoginRequiredMixin, generic.View):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        fieldValue = 'respirationRate'
        results = databaseQuery(fieldValue)

        results = databaseQuerryParser(results, fieldValue)

        averageChange = averageChageCalculation(results)

        maxPostiveChangeVal = maxPostiveChange(results)

        minChangeVal = minChange(results)


        context = { 'averageChange' : averageChange, 'maxPostiveChange' : maxPostiveChangeVal, 'minChange' : minChangeVal}

        return pageUserAuth(request,'Staff',"admin_progress_preview.html",context)

class adminO2SaturationProgressView(LoginRequiredMixin, generic.View):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        fieldValue = 'O2Saturation'
        results = databaseQuery(fieldValue)

        results = databaseQuerryParser(results, fieldValue)

        averageChange = averageChageCalculation(results)

        maxPostiveChangeVal = maxPostiveChange(results)

        minChangeVal = minChange(results)


        context = { 'averageChange' : averageChange, 'maxPostiveChange' : maxPostiveChangeVal, 'minChange' : minChangeVal}

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
        # graph x, y coordinates
        x = [ 1, 2, 3, 4, 5 ]
        y = [ 1, 2, 3, 4, 5 ]

        #setup graph plot
        plot = figure(title= 'Line Graph', x_axis_label= 'X-Axis', y_axis_label= 'Y-Axis', plot_width = 400, plot_height = 400)

        #plot line
        plot.line( x, y, line_width=2 )
        plot.background_fill_color = None
        plot.border_fill_color = None
        #store components
        script, div = components(plot)
        return pageUserAuth(request,'Patient',"patient_progress.html", {'script' : script , 'div': div} )

    


class chatbotPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        return pageUserAuth(request,'Patient',"chatbot.html")

        return render(request, "chatbot.html")

class ChatterBotApiView(generic.View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT)

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(input_data)

        response_data = response.serialize()

        #print(response_data)

        print("*****CHATTERBOTAPIVIEW: POST:*****")
        print("*****CHATTERBOTAPIVIEW: POST: RESPONSEDATA: " + str(response))

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        print("CHATTERBOTAPIVIEW:GET: " + str(self.chatterbot.name))

        return JsonResponse({
            'name': self.chatterbot.name
        })


        

        


