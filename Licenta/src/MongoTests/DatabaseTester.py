'''
Created on Jun 4, 2015

@author: aclosca
'''
import pymongo
import datetime 
import json
from pymongo import MongoClient
from MongoTests.TableGenerator import TableGenerator
from random import randint

class DatabaseTester():
    '''
    classdocs
    '''
    currentNumberOfOps=0
    testTime=0

    def __init__(self, TestConfiguration,NumberOfOperations):
        '''
        Constructor
        '''
        self.NumberOfOperations=NumberOfOperations
        self.TestConfiguration = TestConfiguration
        
    def test(self):
        configuration=self.TestConfiguration
        client = MongoClient()
        db=client.database
        print (db.collection_names());
        readVector=[]
        writeVector=[]
        updateVector=[]
        if 'readState' in configuration:
            for i in range (0,int(configuration['readPercentage'])):
                readVector.append(i+1)
        if 'writeState' in configuration:
            for i in range (0,int(configuration['writePercentage'])):
                writeVector.append(i+1+len(readVector))
        if 'updateState' in configuration:
            for i in range (0,int(configuration['updatePercentage'])):
                updateVector.append(i+1+len(readVector)+len(writeVector))
        now=datetime.datetime.now()
        for i in range(1,int(self.NumberOfOperations)+1):
            random = randint(1,100)
            if random in readVector:
                db.read_collection.find_one({"test":"test"})
            if random in writeVector:
                tb=TableGenerator(configuration,self.NumberOfOperations)
                s=tb.createKeyContentBySize(configuration['writeSize'])
                document=tb.createDocument(configuration['writeKeys'],s)
                db.write_collection.insert(document)
            if  random in updateVector:
                db.update_collection.update({"test":"test"},{"$set":{"test1":"test1"}})
            self.updateCurrentNumberOfOps(i)
            
        later=datetime.datetime.now()
        testTime=later-now
        self.updateTestTime(testTime.seconds)
        print (testTime)
        #db.read_collection.drop()
        #db.update_collection.drop()
        #db.write_collection.drop()
        #client.drop_database('database')
    
    def updateCurrentNumberOfOps(self,currentNumberOfOps):
        self.currentNumberOfOps=currentNumberOfOps
    def updateTestTime(self,testTime):
        self.testTime=testTime
                
            
        
        
        
        
        
        
            
            
        
        
        