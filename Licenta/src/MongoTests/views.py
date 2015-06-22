import threading
import time
import json
import psutil
import os
import collections

from django.forms.models import modelform_factory
from django.forms import ModelForm
from MongoTests.models import TestConfiguration
from django.http import HttpResponse
from django import forms
from django.shortcuts import render
from MongoTests.TableGenerator import TableGenerator
from MongoTests.DatabaseTester import DatabaseTester
from MongoTests.TestConfigurationForm import TestConfigurationForm



        
class myThread (threading.Thread):
    currentNumberOfOps=0
    #time=0
    
    def __init__(self,tester):
        threading.Thread.__init__(self)
        self.tester=tester
    def run(self):
        self.tester.test()
    def getCurrentNumberOfOps(self):
        self.currentNumberOfOps=self.tester.currentNumberOfOps
        return self.currentNumberOfOps
    def getTime(self):
        self.time=self.tester.testTime
        return self.time
    def getThreadId(self):
        return threading.get_ident()
        
        
        
       

        
       
                
       
t1=myThread(0)
isThreadStarted=False;
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
    isFinished=0;
    currentNumberOfOps=0;
    if(isThreadStarted==True):
        
        currentNumberOfOps=t1.getCurrentNumberOfOps()
        data={}
        if not t1.isAlive():
            isFinished=1;
            isThreadStarted=False
            data['testTime']=t1.getTime()
        
        data['currentNumberOfOperation']=currentNumberOfOps;
        

        data['isFinished']=isFinished;
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
    isFinished=0;
    if (isThreadStarted==True):
        isFinished=0;
        proc = psutil.Process()
        data['CPUUsage']=proc.cpu_percent(interval=1)
        data['memoryUsage']=proc.memory_percent()
        data['totalCPUUsage']=psutil.cpu_percent()             
        data['totalMemoryUsage']=psutil.virtual_memory().percent
        data['diskUsage']=psutil.disk_usage('C:/data').percent
        if not t1.isAlive():
            isFinished=1;
            isThreadStarted=False
        data['isFinished']=isFinished;
        return HttpResponse(json.dumps(data),content_type = "application/json");
    else:
        data['CPUUsage']=0
        data['memoryUsage']=0
        data['totalCPUUsage']=psutil.cpu_percent()            
        data['totalMemoryUsage']=psutil.virtual_memory().percent
        data['diskUsage']=psutil.disk_usage('C:/data').percent
        return HttpResponse(json.dumps(data),content_type = "application/json");
def getTestConfiguration(request):
    configuration=request.session["test_configuration"]
    return HttpResponse(json.dumps(configuration),content_type = "application/json");


    

    
