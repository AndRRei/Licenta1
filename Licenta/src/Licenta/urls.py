from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Licenta.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^MongoTests',include('MongoTests.urls')),
    url(r'^admin/', include(admin.site.urls)),
   #url(r'^MongoTests/base', 'MongoTests.views.base'),
   #url(r'^MongoTests/tests', 'MongoTests.views.tests',name='tests'),
    url(r'^MongoTests/dashboard', 'MongoTests.views.dashboard',name='dashboard'),
    url(r'MongoTests/testMongoDB' , 'MongoTests.views.testMongoDB'),
    url(r'MongoTests/saveTestConfiguration',"MongoTests.views.saveTestConfiguration"),
    url(r'MongoTests/getTestStatus','MongoTests.views.getTestStatus'),
    url(r'MongoTests/getCPUUsage','MongoTests.views.getCPUUsage'),
    url(r'MongoTests/getTestConfiguration','MongoTests.views.getTestConfiguration'),
    url(r'MongoTests/generatePdfReport','MongoTests.views.generatePdfReport',name='getPdfReport')
)
