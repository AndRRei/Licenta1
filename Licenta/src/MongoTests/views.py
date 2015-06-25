import threading
import time
import json
import psutil
import os
import collections
import reportlab

from reportlab.rl_config import defaultPageSize  
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.forms.models import modelform_factory
from django.forms import ModelForm
from MongoTests.models import TestConfiguration
from django.http import HttpResponse
from django import forms
from django.shortcuts import render
from MongoTests.TableGenerator import TableGenerator
from MongoTests.DatabaseTester import DatabaseTester
from MongoTests.TestConfigurationForm import TestConfigurationForm
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.graphics.charts.lineplots import GridLinePlot
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import shapes
from reportlab.graphics.charts.axes import XCategoryAxis,YValueAxis





        
class myThread (threading.Thread):
    currentNumberOfOps=0
    intervalsVector=[]
    timesVector=[]
    time=0
    
        
    def __init__(self,tester):
        threading.Thread.__init__(self)
        self.tester=tester
    def run(self):
        self.tester.test()
        self.time=self.tester.testTime
    def getCurrentNumberOfOps(self):
        self.currentNumberOfOps=self.tester.currentNumberOfOps
        return self.currentNumberOfOps
    def getTime(self):
        return self.time
    def getThreadId(self):
        return threading.get_ident()
    def getIntervalsVector(self):
        self.intervalsVector=self.tester.intervalsVector
        self.tester.emptyIntervalsVector()
        return self.intervalsVector
    def getTimesVector(self):
        self.timesVector=self.tester.timesVector
        self.tester.emptyTimesVector()
        return self.timesVector

        
        
       

        
       
                
       
t1=myThread(0)
isThreadStarted=False;
isThreadFinished=0
# def base(request):
#     return render(request , 'base.html')
# def tests(request):
#     return render(request, 'tests.html', {'form': NameForm})
def dashboard(request):
    global t1
    #Stop the thread
    if t1.isAlive():
        tester = DatabaseTester(request.session["test_configuration"],0)
        t1=myThread(tester)
        t1.start()
    Form = modelform_factory(TestConfiguration,form=TestConfigurationForm)
    return render(request,'dashboard.html',{'form':Form})
def saveTestConfiguration(request):
    configuration = TestConfiguration()
    configuration = request.POST
    request.session["test_configuration"]=configuration
    return HttpResponse(json.dumps(configuration),content_type = "application/json");
def testMongoDB(request):
    cr=TableGenerator(request.session["test_configuration"],request.POST.get('NumberOfOperations',False))
    cr.createTables()
    tester = DatabaseTester(request.session["test_configuration"],request.POST.get('NumberOfOperations',False))
    global t1
    t1=myThread(tester)
    t1.start()
    global isThreadStarted
    isThreadStarted=True
    return HttpResponse("Thread for test was started");
def getTestStatus(request):
    global isThreadStarted
    global t1
    currentNumberOfOps=0;
    if(isThreadStarted==True):
        
        isThreadFinished=0;
        currentNumberOfOps=t1.getCurrentNumberOfOps()
        data={}
        if not t1.isAlive():
            isThreadFinished=1;
            isThreadStarted=False
            data['testTime']=t1.getTime()
            data['intervalsVector']=t1.getIntervalsVector()
            data['timesVector']=t1.getTimesVector()
        data['currentNumberOfOperation']=currentNumberOfOps;
        data['isFinished']=isThreadFinished;
        data['isTableCreated']=1
        return HttpResponse(json.dumps(data),content_type = "application/json");
    else:
        data={}
        data['isTableCreated']=0
        return HttpResponse(json.dumps(data),content_type = "application/json");
def getCPUUsage(request):
    data={}
    global isThreadStarted
    global t1
    if (isThreadStarted==True):
        isThreadFinished=0;
        proc = psutil.Process()
        data['CPUUsage']=proc.cpu_percent(interval=1)
        data['memoryUsage']=proc.memory_percent()
        data['diskUsage']=int(psutil.disk_usage('C:/data').used/10e5)
        if not t1.isAlive():
            isThreadFinished=1;
        data['isFinished']=isThreadFinished;
        return HttpResponse(json.dumps(data),content_type = "application/json");
    else:
        data['CPUUsage']=0
        data['memoryUsage']=0
        data['diskUsage']=int(psutil.disk_usage('C:/data').used/10e5)
        return HttpResponse(json.dumps(data),content_type = "application/json");
def getTestConfiguration(request):
    configuration=request.session["test_configuration"]
    return HttpResponse(json.dumps(configuration),content_type = "application/json");
def generatePdfReport(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)
    
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    Title="Test Report"
    PAGE_HEIGHT=defaultPageSize[1]  
    PAGE_WIDTH=defaultPageSize[0]  
    p.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
    p.drawString(100,900,"Test Configuration")
    configuration=request.session["test_configuration"]
    data=[['Operation','On/Off','Percentage','Keys','Size']]
    if 'readState' in configuration:
        readData=[['Read',configuration['readState'],configuration['readPercentage'],configuration['readKeys'],configuration['readSize']]]
    else:
        readData=[['Read','0','0','0','0']]
    data=data+readData
    if 'writeState' in configuration:
        writeData=[['Write',configuration['writeState'],configuration['writePercentage'],configuration['writeKeys'],configuration['writeSize']]]
    else:
        writeData=[['Write','0','0','0','0']]
    data=data+writeData
    if 'updateState' in configuration:
        updateData=[['Update',configuration['updateState'],configuration['updatePercentage'],configuration['updateKeys'],configuration['updateSize']]]
    else:
        updateData=[['Update','0','0','0','0']]
    data=data+updateData
    table = Table(data, colWidths=100, rowHeights=20)
    table.hAlign="CENTER"
    table.setStyle(TableStyle())
    table.wrapOn(p, 300, 800)
    table.drawOn(p,80,550)
    
    p.drawString(80,700,"Test Configuration")
    p.drawString(80,500,"Test Time : ")
    p.drawString(200,500,str(t1.getTime()) + " miliseconds " )
    p.drawString(80,400,"Test Chart")
    p.saveState()
    
    drawing = Drawing(10, 10)
    data = [(10, 20, 30, 40), (15, 22, 37, 42)]
    xAxis = XCategoryAxis()
    xAxis.setPosition(75, 75, 300)
    xAxis.configure(data)
    xAxis.categoryNames = ['Beer', 'Wine', 'Meat', 'Cannelloni']
    xAxis.labels.boxAnchor = 'n'
    xAxis.labels[3].dy = -15
    xAxis.labels[3].angle = 30
    xAxis.labels[3].fontName = 'Times-Bold'
    yAxis = YValueAxis()
    yAxis.setPosition(50, 50, 125)
    yAxis.configure(data)
    drawing.add(xAxis)
    drawing.add(yAxis)
    
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


    

    
