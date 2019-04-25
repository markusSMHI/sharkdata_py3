"""sharkdata_py3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
# 
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.conf.urls import include, url
import app_sharkdata_base.views

urlpatterns = [
    url(r'^about/', app_sharkdata_base.views.viewAbout),
    url(r'^documentation/',app_sharkdata_base.views.viewDocumentation),
    url(r'^examplecode/', app_sharkdata_base.views.viewExampleCode),
    url(r'^datapolicy/', app_sharkdata_base.views.viewDataPolicy),
    #
    url(r'^datasets/', include('app_datasets.urls')),
    url(r'^ctdprofiles/', include('app_ctdprofiles.urls')),
    url(r'^resources/', include('app_resources.urls')),
    url(r'^exportformats/', include('app_exportformats.urls')),
    url(r'^speciesobs/', include('app_speciesobs.urls')),
    url(r'^sharkdataadmin/', include('app_sharkdataadmin.urls')), 
    #
    url(r'^', include('app_datasets.urls')), # Default page.
]
