'''
Created on Jun 22, 2015

@author: aclosca
'''

from django.forms import ModelForm
from MongoTests.models import TestConfiguration

class TestConfigurationForm(ModelForm):
    class Meta:
        model =TestConfiguration
        fields =['readState','readPercentage','readKeys','readSize',
                    'writeState','writePercentage','writeKeys','writeSize',
                    'updateState','updatePercentage','updateKeys','updateSize']