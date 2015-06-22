from django.db import models

class TestConfiguration(models.Model):
        readState = models.BooleanField()
        readPercentage=models.CharField(max_length=200)
        readKeys=models.CharField(max_length=200)
        readSize=models.CharField(max_length=200)
        
        writeState= models.BooleanField()
        writePercentage=models.CharField(max_length=200)
        writeKeys=models.CharField(max_length=200)
        writeSize=models.CharField(max_length=200)
        
        updateState= models.BooleanField()
        updatePercentage=models.CharField(max_length=200)
        updateKeys=models.CharField(max_length=200)
        updateSize=models.CharField(max_length=200)
    