#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import datetime

from django.http import HttpResponse,HttpResponseRedirect
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
# import django.core.paginator as paginator
from django.conf import settings

from app_sharkdataadmin import forms
import app_exportformats.models as exportformats_models
import sharkdata_core


##### Exportfiles,DarwinCore-Archive. #####

def deleteDwcaExportFiles(request):
    """ Delete all DarwinCore-Archive files from the 'Export formats' page. """
    error_message = None
    #
    if request.method == "GET":
        #
        form = forms.DeleteDwcaExportFilesForm()
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("delete_dwca_exportfiles.html", contextinstance)
    elif request.method == "POST":
        #
        form = forms.DeleteDwcaExportFilesForm(request.POST)
        if form.is_valid():
            #
            user = request.POST['user']
            password = request.POST['password']
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
            if error_message == None:
                logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Delete all DwC-A files', user=user) 
                try:
                    exportformats_models.ExportFiles.objects.all().filter(format = 'DwC-A').delete()
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                except:
                    error_message = u"Can't delete DarwinCore-Archive files."
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
            
            if error_message == None:
                return HttpResponseRedirect("/sharkdataadmin")
        #
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("delete_dwca_exportfiles.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/sharkdataadmin")

def generateDwcaExportFiles(request):
    """ Generates DarwinCore-Archive files for the 'Export formats' page. """
    error_message = None
    #
    if request.method == "GET":
        form = forms.GenerateDwcaExportFilesForm()
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("generate_dwca_exportfiles.html", contextinstance)
    elif request.method == "POST":
        #
        form = forms.GenerateDwcaExportFilesForm(request.POST)
        if form.is_valid():
            #
            datatype_list = []
            year_from = request.POST['year_from']
            year_to = request.POST['year_to']
            monitoring_type = request.POST['monitoring_type']
            user = request.POST['user']
            password = request.POST['password']
            #
            if ('phytobenthos' in request.POST) and (request.POST['phytobenthos'] == 'on'):
                datatype_list.append('Epibenthos')
#                 datatype_list.append('Phytobenthos')
            if ('phytoplankton' in request.POST) and (request.POST['phytoplankton'] == 'on'):
                datatype_list.append('Phytoplankton')
            if ('zoobenthos' in request.POST) and (request.POST['zoobenthos'] == 'on'):
                datatype_list.append('Zoobenthos')
            if ('zooplankton' in request.POST) and (request.POST['zooplankton'] == 'on'):
                datatype_list.append('Zooplankton')
            #
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
            if error_message == None:
                    sharkdata_core.SharkdataAdminUtils().generateDwcaExportFilesInThread(
                                                    datatype_list, year_from, year_to, monitoring_type, user)
            # OK.
            if error_message == None:
                return HttpResponseRedirect("/sharkdataadmin")
        #
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("generate_dwca_exportfiles.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/sharkdataadmin")

##### Exportfiles, ICES-XML. #####

def deleteIcesXmlExportFiles(request):
    """ Delete all DarwinCore-Archive files from the 'Export formats' page. """
    error_message = None
    #
    if request.method == "GET":
        #
        form = forms.DeleteIcesXmlExportFilesForm()
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("delete_ices_xml_exportfiles.html", contextinstance)
    elif request.method == "POST":
        #
        form = forms.DeleteIcesXmlExportFilesForm(request.POST)
        if form.is_valid():
            #
            user = request.POST['user']
            password = request.POST['password']
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
            if error_message == None:
                logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Delete all ICES-XML files', user=user)
                try:
                    exportformats_models.ExportFiles.objects.all().filter(format = 'ICES-XML').delete()
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                except:
                    error_message = u"Can't delete datasets from the database."
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
            # OK.
            if error_message == None:
                return HttpResponseRedirect("/sharkdataadmin")
        #
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("delete_ices_xml_exportfiles.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/sharkdataadmin")

def generateIcesXmlExportFiles(request):
    """ Generates ICES-XML files for the 'Export formats' page. """
    error_message = None
    #
    if request.method == "GET":
        form = forms.GenerateIcesXmlExportFilesForm()
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("generate_ices_xml_exportfiles.html", contextinstance)
    elif request.method == "POST":
        #
        form = forms.GenerateIcesXmlExportFilesForm(request.POST)
        if form.is_valid():
            #
            datatype_list = []
            year_from = request.POST['year_from']
            year_to = request.POST['year_to']
            status = request.POST['status']
            user = request.POST['user']
            password = request.POST['password']
            #
            if ('phytobenthos' in request.POST) and (request.POST['phytobenthos'] == 'on'):
                datatype_list.append('Epibenthos')
#                 datatype_list.append('Phytobenthos')
            if ('phytoplankton' in request.POST) and (request.POST['phytoplankton'] == 'on'):
                datatype_list.append('Phytoplankton')
            if ('zoobenthos' in request.POST) and (request.POST['zoobenthos'] == 'on'):
                datatype_list.append('Zoobenthos')
            if ('zooplankton' in request.POST) and (request.POST['zooplankton'] == 'on'):
                datatype_list.append('Zooplankton')
            #
# #             if ('Phytobenthos' in datatype_list) or \
#             if ('Phytoplankton' in datatype_list) or \
#                ('Zooplankton' in datatype_list):
#                 error_message = 'Support for Zoobenthos only, others are under development. Please try again...'   
            #
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
            if error_message == None:
                    sharkdata_core.SharkdataAdminUtils().generateIcesXmlExportFilesInThread(
                                                    datatype_list, year_from, year_to, status, user)
            # OK.
            if error_message == None:
                return HttpResponseRedirect("/sharkdataadmin")
        #
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("generate_ices_xml_exportfiles.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/sharkdataadmin")

def validateIcesXmlExportFiles(request):
    """ Validate ICES-XML files on the 'Export formats' page. """
    error_message = None
    #
    if request.method == "GET":
        form = forms.ValidateIcesXmlForm()
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("validate_ices_xml_exportfiles.html", contextinstance)
    elif request.method == "POST":
        #
        form = forms.ValidateIcesXmlForm(request.POST)
        if form.is_valid():
            #
            datatype_list = []
            user = request.POST['user']
            password = request.POST['password']
            #
            if ('phytobenthos' in request.POST) and (request.POST['phytobenthos'] == 'on'):
                datatype_list.append('Phytobenthos')
                datatype_list.append('Epibenthos')
            if ('phytoplankton' in request.POST) and (request.POST['phytoplankton'] == 'on'):
                datatype_list.append('Phytoplankton')
            if ('zoobenthos' in request.POST) and (request.POST['zoobenthos'] == 'on'):
                datatype_list.append('Zoobenthos')
            if ('zooplankton' in request.POST) and (request.POST['zooplankton'] == 'on'):
                datatype_list.append('Zooplankton')
            #
#             if ('Phytobenthos' in datatype_list) or \
#                ('Phytoplankton' in datatype_list) or \
#                ('Zooplankton' in datatype_list):
#                 error_message = 'Support for Zoobenthos only, others are under development. Please try again...'   
            #
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
            if error_message == None:
                    sharkdata_core.SharkdataAdminUtils().validateIcesXmlInThread(datatype_list, user)
            # OK.
            if error_message == None:
                return HttpResponseRedirect("/sharkdataadmin")
        #
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("validate_ices_xml_exportfiles.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/sharkdataadmin")

##### Admin page and log. #####

def sharkDataAdmin(request):
    """ """
    per_page = 5
    try:
        if 'per_page' in request.GET:
            per_page = int(request.GET['per_page'])
    except:
        pass
    
    logrows = []
    log_file_list = sharkdata_core.SharkdataAdminUtils().get_log_files()
    log_file_list = log_file_list[0:per_page]
    
    for log_file in sorted(log_file_list, reverse=True):
        
        log_file_path = pathlib.Path(log_file)
        stem = log_file_path.stem
        parts = stem.split('_')
        
        date = parts[0]
        time = parts[1]
        command = ' '.join(parts[2:-1])
        status = parts[-1]

        logrow = {}
        logrow['date'] = date
        logrow['time'] = time
        logrow['started_datetime'] = datetime.datetime.strptime(date + ' ' +  time, '%Y-%m-%d %H%M%S')
        logrow['command_name'] = command
        logrow['status'] = status
        logrow['file_stem'] = stem
        
        logrows.append(logrow)
    #
    return render_to_response("sharkdata_admin.html",
                              {'logrows' : logrows})

def viewLog(request, file_stem):
    """ """
    log_content = ''
    try:
        log_content = sharkdata_core.SharkdataAdminUtils().get_log_file_content(file_stem)
    except:
        pass
    #
    response = HttpResponse(content_type = 'text/plain; charset=cp1252')    
    response.write(log_content.encode('cp1252'))
    return response

##### Datasets and resources. #####

def updateDatasetsAndResources(request):
    """ Updates the database from datasets and resources stored in the FTP area.
    """
    error_message = None
    #
    if request.method == "GET":
        form = forms.UpdateDatasetsAndResourcesForm()
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("update_datasets_and_resources.html", contextinstance)
    elif request.method == "POST":
        #
        form = forms.UpdateDatasetsAndResourcesForm(request.POST)
        if form.is_valid():
            #
            user = request.POST['user']
            password = request.POST['password']
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            # Load datasets.
            if error_message == None:
                sharkdata_core.SharkdataAdminUtils().updateDatasetsAndResourcesInThread(user)
            # OK.
            if error_message == None:
                return HttpResponseRedirect("/sharkdataadmin")
        #
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("update_datasets_and_resources.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/sharkdataadmin")

##### Species observations. #####

def updateSpeciesObs(request):
    """ Updates species observations based of content in the datasets. """
    error_message = None
    #
    if request.method == "GET":
        #
        form = forms.UpdateSpeciesObsForm()
        contextinstance = {'form': form,
                           'error_message': error_message}
        contextinstance.update(csrf(request))
        return render_to_response("speciesobs_update.html", contextinstance)
    elif request.method == "POST":
        form = forms.UpdateSpeciesObsForm(request.POST)
        if form.is_valid():
            #
            user = request.POST['user']
            password = request.POST['password']
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
            if error_message == None:
                logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Update species observations', user=user)
                try:
                    error_message = sharkdata_core.SharkdataAdminUtils().updateSpeciesObsInThread(logfile_name)
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                except:
                    error_message = u"Can't update species observations from datasets."
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
            # OK.
            if error_message == None:
                return HttpResponseRedirect("/sharkdataadmin")
        #
        contextinstance = {'form': form,
                           'error_message': error_message}
        contextinstance.update(csrf(request))
        return render_to_response("speciesobs_update.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/sharkdataadmin")

def cleanUpSpeciesObs(request):
    """ Removes species observations with status='DELETED'. """
    error_message = None
    #
    if request.method == "GET":
        #
        form = forms.CleanUpSpeciesObsForm()
        contextinstance = {'form': form,
                           'error_message': error_message}
        contextinstance.update(csrf(request))
        return render_to_response("speciesobs_cleanup.html", contextinstance)
    elif request.method == "POST":
        form = forms.CleanUpSpeciesObsForm(request.POST)
        if form.is_valid():
            #
            user = request.POST['user']
            password = request.POST['password']
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
            if error_message == None:
                logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Clean up species observations', user=user)
                try:
                    error_message = sharkdata_core.SharkdataAdminUtils().cleanUpSpeciesObsInThread(logfile_name)
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                except:
                    error_message = u"Can't clean up species observations."
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
            # 
            if error_message == None:
                return HttpResponseRedirect("/sharkdataadmin")
        #
        contextinstance = {'form': form,
                           'error_message': error_message}
        contextinstance.update(csrf(request))
        return render_to_response("speciesobs_cleanup.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/sharkdataadmin")


