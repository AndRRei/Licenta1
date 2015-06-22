'''
Created on 26.03.2015

@author: Closca
'''
from celery import Celery
import time

app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def runOperations(numOfOperations):
    totalNumOfOperations=numOfOperations
    currentNumOfOperations=0
    status=0
    totalNumOfOperations=totalNumOfOperations
    time.sleep(1)
    status=1
    time.sleep(2)
    currentNumOfOperations=totalNumOfOperations/5
    status=currentNumOfOperations 
    time.sleep(3)
    currentNumOfOperations=totalNumOfOperations/4
    status=currentNumOfOperations 
    time.sleep(4)
    currentNumOfOperations=totalNumOfOperations/3
    status=currentNumOfOperations 
    time.sleep(5)
    currentNumOfOperations=totalNumOfOperations/2
    status=currentNumOfOperations 
    time.sleep(6)
    currentNumOfOperations=totalNumOfOperations
    status=currentNumOfOperations
     
    