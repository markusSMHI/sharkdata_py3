#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from django.conf import settings
import app_resources.models as models
import app_resources.forms as forms
# import app_sharkdataadmin.models as admin_models
import sharkdata_core

def resourceContentText(request, resource_name):
    """ Returns data in text format for a specific resource. """
    resource = models.Resources.objects.get(resource_name = resource_name)
    data_as_text = resource.file_content
    resource_file_name = resource.resource_file_name
    #
    response = HttpResponse(content_type = 'text/plain; charset=cp1252')    
    response['Content-Disposition'] = 'attachment; filename=' + resource_file_name   
    response.write(data_as_text.encode('cp1252'))
    return response

def listResources(request):
    """ Generates an HTML page listing all resources. """
    resources = models.Resources.objects.all().order_by('resource_name')
    #
    return render_to_response("list_resources.html",
                              {'resources' : resources})

def listResourcesJson(request):
    """ Generates a JSON file containing a list of resources and their properties. """
    data_header = sharkdata_core.ResourcesUtils().getHeaders()
    resources_json = []
    #
    data_rows = models.Resources.objects.values_list(*data_header)
    for data_row in data_rows:
        row_dict = dict(zip(data_header, data_row))
        resources_json.append(row_dict)
    #
    response = HttpResponse(content_type = 'application/json; charset=cp1252')
    response['Content-Disposition'] = 'attachment; filename=sharkdata_resource_list.json'    
    response.write(json.dumps(resources_json, encoding = 'utf8'))
    return response
    
def tableResourcesText(request):
    """ Generates a text file containing a list of resources and their properties. """
    data_header = sharkdata_core.ResourcesUtils().getHeaders()
    translated_header = sharkdata_core.ResourcesUtils().translateHeaders(data_header)
    #
    data_rows = models.Resources.objects.values_list(*data_header)
    #
    response = HttpResponse(content_type = 'text/plain; charset=cp1252')    
    response['Content-Disposition'] = 'attachment; filename=sharkdata_resources.txt'    
    response.write('\t'.join(translated_header) + '\r\n') # Tab separated.
    for row in data_rows:
        response.write('\t'.join(row) + '\r\n') # Tab separated.        
    return response

def tableResourcesJson(request):
    """ Generates a text file containing a list of resources and their properties. 
        Organised as header and rows.
    """
    data_header = sharkdata_core.ResourcesUtils().getHeaders()
    #
    data_rows = models.Resources.objects.values_list(*data_header)
    #
    response = HttpResponse(content_type = 'application/json; charset=cp1252')
    response['Content-Disposition'] = 'attachment; filename=sharkdata_resources.json'    
    response.write('{')
    response.write('"header": ["')
    response.write('", "'.join(data_header) + '"], ') # Tab separated.
    response.write(u"'rows': [")
    row_delimiter = ''
    for row in data_rows:
        response.write(row_delimiter + '["' + '", "'.join(row) + '"]')      
        row_delimiter = ', '
    response.write(']')
    response.write('}')
    #
    return response

def deleteResource(request, resource_id):
    """ Deletes one row in the database. The FTP area is not affected. """
    resource = models.Resources.objects.get(id=resource_id)
    #
    if request.method == "GET":
        form = forms.DeleteResourceForm()
        contextinstance = {'form'   : form,
                           'resource' : resource,
                           'error_message' : None}
        contextinstance.update(csrf(request))
        return render_to_response("delete_resource.html",  contextinstance)
    elif request.method == "POST":
        # Reloads db-stored data.
        sharkdata_core.ResourcesUtils().clear()
        #
        error_message = None # initially.
        #
        form = forms.DeleteResourceForm(request.POST)
        if form.is_valid():
            #
            user = request.POST['user']
            if user not in settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.keys():
                error_message = 'Not a valid user. Please try again...'   
            #
            if error_message == None:
                logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Delete resource', user=user)
                if ('delete_ftp' in request.POST) and (request.POST['delete_ftp'] == 'on'):
                    try:
                        sharkdata_core.ResourcesUtils().deleteFileFromFtp(resource.resource_file_name)
                        sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, 
                                                                       log_row='Resource deleted from the FTP area: ' + resource.resource_file_name)
                    except:
                        error_message = "Can't delete resources from the FTP area. File: " + resource.resource_file_name
                        sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                        sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
            
            if error_message == None:
                try:
                    resource = models.Resources.objects.get(id=resource_id)
                    resource.delete()
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, 
                                                                   log_row='Resource deleted from DB: ' + resource.resource_file_name)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                except:
                    error_message = "Can't delete resources from the database. File: " + resource.resource_file_name
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
            # 
            if error_message == None:
                return HttpResponseRedirect("/resources")
        #
        contextinstance = {'form'   : form,
                           'resource' : resource,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("delete_resource.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/resources")
