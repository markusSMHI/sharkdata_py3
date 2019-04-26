#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# import json
from django.http import HttpResponse,HttpResponseRedirect
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
# import django.core.paginator as paginator
from django.conf import settings

from app_sharkdataadmin import forms
# import app_sharkdataadmin.models as admin_models
import app_datasets.models as datasets_models
import app_resources.models as resources_models
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
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.get(user, None):
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
# #             if ('Phytobenthos' in datatype_list) or \
#             if ('Phytoplankton' in datatype_list) or \
#                ('Zooplankton' in datatype_list):
#                 error_message = 'Support for Zoobenthos only, others are under development. Please try again...'   
            #
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.get(user, None):
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
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
#             if error_message == None:
#                 if ('delete_ftp' in request.POST) and (request.POST['delete_ftp'] == 'on'):
#                     logrow_id = admin_models.createLogRow(command = 'Delete all datasets from FTP', status = 'RUNNING', user = user)
#                     try:
#                         error_message = dataset_utils.DatasetUtils().deleteAllFilesFromFtp()
#                         admin_models.changeLogRowStatus(logrow_id, status = 'FINISHED')
#                     except:
#                         error_message = u"Can't delete datasets from the FTP area."
#                         admin_models.changeLogRowStatus(logrow_id, status = 'FAILED')
#                         admin_models.addResultLog(logrow_id, result_log = error_message)
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
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.get(user, None):
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
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.get(user, None):
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
    log_rows_per_page = 5
    try:
        if 'log_rows_per_page' in request.GET:
            log_rows_per_page = int(request.GET['log_rows_per_page'])
    except:
        pass
    
#     logrows = admin_models.CommandLog.objects.all().order_by('-id')[:log_rows_per_page] # Reverse order.
    logrows = []
    #
    return render_to_response("sharkdata_admin.html",
                              {'logrows' : logrows})

def viewLog(request, log_id):
    """ """
#     command_log = admin_models.CommandLog.objects.get(id=log_id)
#     result_log = command_log.result_log
    result_log = ''
    #
    response = HttpResponse(content_type = 'text/plain; charset=cp1252')    
    response.write(result_log.encode('cp1252'))
    return response

##### Datasets. #####

def deleteDatasets(request):
    """ Deletes all rows in the database. """
    error_message = None
    #
    if request.method == "GET":
        #
        form = forms.DeleteAllDatasetsForm()
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("delete_datasets.html", contextinstance)
    elif request.method == "POST":
        #
        form = forms.DeleteAllDatasetsForm(request.POST)
        if form.is_valid():
            #
            user = request.POST['user']
            password = request.POST['password']
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
            if error_message == None:
                if ('delete_ftp' in request.POST) and (request.POST['delete_ftp'] == 'on'):
                    logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Delete all datasets from FTP area', user=user)
                    try:
                        error_message = sharkdata_core.DatasetUtils().deleteAllFilesFromFtp()
                        sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
                        sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                    except:
                        error_message = u"Can't delete datasets from the FTP area."
                        sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                        sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
            #
            if error_message == None:
                logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Delete all datasets', user=user)
                try:
                    datasets_models.Datasets.objects.all().delete()
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
        return render_to_response("delete_datasets.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/sharkdataadmin")

def loadDatasets(request):
    """ Updates the database from datasets stored in the FTP area.
        I multiple versions of a dataset are in the FTP area only the latest 
        will be loaded.
    """
    error_message = None
    #
    if request.method == "GET":
        form = forms.LoadAllDatasetsForm()
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("load_datasets.html", contextinstance)
    elif request.method == "POST":
        #
        form = forms.LoadAllDatasetsForm(request.POST)
        if form.is_valid():
            #
            user = request.POST['user']
            password = request.POST['password']
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            # Load datasets.
            if error_message == None:
                logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Load all datasets', user=user)
                try:
                    error_counter = sharkdata_core.DatasetUtils().writeLatestDatasetsInfoToDb(logfile_name, user)
                    if error_counter > 0:
                        sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED Errors:' + str(error_counter))
                    else:
                        sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                except Exception as e:
                    error_message = u"Can't load datasets and save to the database."
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
                        
                        
                    if settings.DEBUG: print('\nError: ' + error_message + '\nException: ' + str(e) + '\n')
                    settings.LOGGER.error('\nError: ' + error_message + '\nException: ' + str(e) + '\n')                    
            # Delete old versions of dataset files.
            if error_message == None:
                if ('delete_old_ftp_versions' in request.POST) and (request.POST['delete_old_ftp_versions'] == 'on'):
                    try:
                        error_counter = sharkdata_core.DatasetUtils().deleteOldFtpVersions(logfile_name, user)
                        if error_counter > 0:
                            sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED Errors:' + str(error_counter))
                        else:
                            sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                    except Exception as e:
                        error_message = u"Can't delete old versions in the FTP area."
                        sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                        sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
                        if settings.DEBUG: 
                            print('\nError: ' + error_message + '\nException: ' + str(e) + '\n')
                            settings.LOGGER.error('\nError: ' + error_message + '\nException: ' + str(e) + '\n')                    
            # OK.
            if error_message == None:
                return HttpResponseRedirect("/sharkdataadmin")
        #
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("load_datasets.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/sharkdataadmin")

##### Resources. #####

def deleteResources(request):
    """ Deletes all rows in the database. The FTP area is not affected. """
    error_message = None
    #
    if request.method == "GET":
        #
        form = forms.DeleteAllResourcesForm()
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("delete_resources.html", contextinstance)
    elif request.method == "POST":
        # Reloads db-stored data.
        sharkdata_core.ResourcesUtils().clear()
        #
        form = forms.DeleteAllResourcesForm(request.POST)
        if form.is_valid():
            #
            user = request.POST['user']
            password = request.POST['password']
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
            if error_message == None:
                if ('delete_ftp' in request.POST) and (request.POST['delete_ftp'] == 'on'):
                    logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Delete all resources from FTP area', user=user)
                    try:
                        sharkdata_core.ResourcesUtils().deleteAllFilesFromFtp()
                        sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
                        sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                    except:
                        error_message = u"Can't delete resources from the database."
                        sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                        sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
            #
            if error_message == None:
                logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Delete all resources', user=user)
                try:
                    resources_models.Resources.objects.all().delete()
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                except:
                    error_message = u"Can't delete resources from the database."
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
            #
            if error_message == None:
                return HttpResponseRedirect("/sharkdataadmin")
        #
        contextinstance = {'form'   : form,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render_to_response("delete_resources.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/sharkdataadmin")

def loadResources(request):
    """ Updates the database from resources stored in the FTP area.
    """
    error_message = None
    #
    if request.method == "GET":
        form = forms.LoadAllResourcesForm()
        contextinstance = {'form': form,
                           'error_message': error_message}
        contextinstance.update(csrf(request))
        return render_to_response("load_resources.html", contextinstance)
    elif request.method == "POST":
        # Reloads db-stored data.
        sharkdata_core.ResourcesUtils().clear()
        #
        form = forms.LoadAllResourcesForm(request.POST)
        if form.is_valid():
            #
            user = request.POST['user']
            password = request.POST['password']
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
            if error_message == None:
                logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Load all resources', user=user)
                try:
                    sharkdata_core.ResourcesUtils().writeResourcesInfoToDb(user)
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                except Exception as e:
                    error_message = u"Can't load resources and save to the database."
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
            # 
            if error_message == None:
                return HttpResponseRedirect("/sharkdataadmin")
        #
        contextinstance = {'form': form,
                           'error_message': error_message}
        contextinstance.update(csrf(request))
        return render_to_response("load_resources.html", contextinstance)
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
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.get(user, None):
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
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
            if error_message == None:
                logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Clean up species observations', user=user)
                try:
                    error_message = sharkdata_core.SharkdataAdminUtils().cleanUpSpeciesObsInThread(logfile_name)
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                    # admin_models.changeLogRowStatus(logrow_id, status = 'FINISHED')
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


##### DarwinCore-Archive for each dataset. #####

# def generateArchives(request):
#     """ Generates archive files (DwC-A) for all datasets.
#     """
#     error_message = None
#     #
#     if request.method == "GET":
#         form = forms.GenerateArchivesForm()
#         contextinstance = {'form'   : form,
#                            'error_message' : error_message}
#         contextinstance.update(csrf(request))
#         return render_to_response("generate_archives.html", contextinstance)
#     elif request.method == "POST":
#         #
#         form = forms.GenerateArchivesForm(request.POST)
#         if form.is_valid():
#             #
#             user = request.POST['user']
#             password = request.POST['password']
#             if password != settings.APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST.get(user, None):
#                 error_message = 'Not a valid user or password. Please try again...'   
#             #
#             if error_message == None:
#                     sharkdata_core.SharkdataAdminUtils().generateArchivesForAllDatasetsInThread(user)
#             # OK.
#             if error_message == None:
#                 return HttpResponseRedirect("/sharkdataadmin")
#         #
#         contextinstance = {'form'   : form,
#                            'error_message' : error_message}
#         contextinstance.update(csrf(request))
#         return render_to_response("generate_archives.html", contextinstance)
#     # Not a valid request method.
#     return HttpResponseRedirect("/sharkdataadmin")
    
