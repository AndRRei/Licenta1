'''
Created on Jun 3, 2015

@author: aclosca
'''
import pymongo

from pymongo import MongoClient

class TableGenerator():
    '''
    classdocs
    '''


    def __init__(self, TestConfiguration,NumberOfOperations):
        '''
        Constructor
        '''
        self.NumberOfOperations=NumberOfOperations
        self.TestConfiguration=TestConfiguration
    
    def createTables(self):

        configuration=self.TestConfiguration
        client = MongoClient()
        client.drop_database('database')
        db=client.database
        db.read_collection.drop()
        db.update_collection.drop()
        db.write_collection.drop()
        if 'readState' in configuration:
            db.read_collection.insert_one({"create":"readCollection"})
            documents=self.createDocuments(int(int(self.NumberOfOperations) * float(int(configuration['readPercentage'])*0.01)),configuration['readSize'],configuration['readKeys'])
            db.read_collection.insert_many(documents)
        if 'writeState' in configuration:
            db.write_collection.insert_one({"create":"writeCollection"})
        if 'updateState' in configuration:
            db.update_collection.insert_one({"create":"updateCollection"})
            documents=self.createDocuments(int(int(self.NumberOfOperations) * float(int(configuration['updatePercentage'])*0.01)),configuration['updateSize'],configuration['updateKeys'])
            db.update_collection.insert_many(documents)
    def createDocument(self,numberOfKeys,s):
        document = {}
        key=""
        for i in range (0,int(numberOfKeys)):
            key ="key" + str(i)
            document.update({key : s})
        return document    
        
    def createKeyContentBySize(self,keySize):
        s=""
        for i in range(0,int(keySize)):
            s+="a"
        return s
    def createDocuments(self,NumberOfOperations,keySize,numberOfKeys):
        s=self.createKeyContentBySize(keySize)
        documents =[]
        for i in range (0,int(NumberOfOperations)):
            document=self.createDocument(numberOfKeys,s)
            documents.append(document)
        return documents 
    def printCollection(self,collection):
        for document in collection.find():
            print (document)    
            
        
    
        
        
            
    
        