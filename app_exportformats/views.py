#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import json
import codecs

from django.http import HttpResponse, HttpResponseRedirect #, StreamingHttpResponse
from django.template.context_processors import csrf
from django.shortcuts import render
from django.conf import settings
# from wsgiref.util import FileWrapper
from django.core import paginator
from app_exportformats import models
from app_exportformats import forms
# import app_sharkdataadmin.models as admin_models

import sharkdata_core

def icesHarvestXml(request):
    """ """
    # URL parameters.
    create_date = request.GET.get('create_date', False)
    monitoring_year = request.GET.get('monitoring_year', False)
    datatype = request.GET.get('datatype', False)
    
    data_header = [
        'format', 
        'datatype', 
        'year', 
        'status', 
        'approved', 
        'export_name', 
        'export_file_name', 
        'generated_datetime', 
        ]
    #
    exportfiles_json = []
    #
    data_rows = models.ExportFiles.objects.values_list(*data_header).order_by('-generated_datetime')
    for data_row in data_rows:
        row_dict = dict(zip(data_header, map(str, data_row)))
        exportfiles_json.append(row_dict)
    #
    harvest_xml_content = sharkdata_core.IcesHarvestXml().approved_icex_exports_listed_in_xml(exportfiles_json,
                                                                                              create_date_filter = create_date, 
                                                                                              monitoring_year_filter = monitoring_year, 
                                                                                              datatype_filter = datatype)
    #
    response = HttpResponse(content_type = 'application/xml; charset=cp1252')    
    response['Content-Disposition'] = 'attachment; filename=' + 'ices_harvest.xml'    
    response.write(harvest_xml_content)
    return response

# def icesHarvestXml(request):
#     """ """
#     data_header = [
#         'format', 
#         'datatype', 
#         'year', 
#         'status', 
#         'approved', 
#         'export_name', 
#         'export_file_name', 
#         'generated_datetime', 
#         ]
#     #
#     exportfiles_json = []
#     #
#     data_rows = models.ExportFiles.objects.values_list(*data_header).order_by('-generated_datetime')
#     for data_row in data_rows:
#         row_dict = dict(zip(data_header, map(str, data_row)))
#         exportfiles_json.append(row_dict)
#     #
#     harvest_xml_content = sharkdata_core.IcesHarvestXml().approved_icex_exports_listed_in_xml(exportfiles_json)
#     #
#     response = HttpResponse(content_type = 'application/xml; charset=cp1252')    
#     response['Content-Disposition'] = 'attachment; filename=' + 'ices_harvest.xml'    
#     response.write(harvest_xml_content)
#     return response

def IcesXml(request, export_name):
    """ Returns ICES XML file. """
    #
    exportfile = models.ExportFiles.objects.get(export_name = export_name)
    export_file_name  = exportfile.export_file_name
    export_file_path  = exportfile.export_file_path
    #
    file_content = ''
    try:
        export_file = codecs.open(export_file_path, 'r', encoding = 'cp1252')
        file_content = export_file.read()
        export_file.close()
    except:
        pass
    #
    if '.xml' in export_file_name:
        response = HttpResponse(content_type = 'application/xml; charset=cp1252')
    else:    
        response = HttpResponse(content_type = 'text/plain; charset=cp1252')
        
    response['Content-Disposition'] = 'attachment; filename=' + export_file_name    
    response.write(file_content)
    return response

def IcesXmlLog(request, export_name):
    """ Returns ICES XML log file. """
    #
    exportfile = models.ExportFiles.objects.get(export_name = export_name)
#     error_log_file  = exportfile.error_log_file
    error_log_file_path  = exportfile.error_log_file_path
    #
    file_content = '<Log file not available.>'
    try:
        log_file = codecs.open(error_log_file_path, 'r', encoding = 'cp1252')
        file_content = log_file.read()
        log_file.close()
    except:
        pass
    #
    response = HttpResponse(content_type = 'text/plain; charset=cp1252')    
#     response['Content-Disposition'] = 'attachment; filename=' + error_log_file    
    response.write(file_content)
    return response

def listExportFiles(request):
    """ Generates an HTML page listing all ExportFiles. """

    # URL parameters.
    per_page_default = 10
    try:
        pagination_page = int(request.GET.get('page', 1))
    except:
        pagination_page = 1
    try:
        pagination_size = int(request.GET.get('per_page', per_page_default))
    except:
        pagination_size = per_page_default    
    selected_format = request.GET.get('format', 'All')
    #
    if (selected_format and (selected_format != 'All')):
#         exportfiles = models.ExportFiles.objects.all().filter(format = selected_format).order_by('export_file_name')
        exportfiles = models.ExportFiles.objects.all().filter(format = selected_format).order_by('-generated_datetime')
    else:
#         exportfiles = models.ExportFiles.objects.all().order_by('export_file_name')
        exportfiles = models.ExportFiles.objects.all().order_by('-generated_datetime')
    #
    formats = models.ExportFiles.objects.values_list('format').distinct().order_by('format')
    format_list = []
    for format_item in formats:
        try:
            format_list.append(format_item[0])
        except:
            pass
    #
    pag = paginator.Paginator(exportfiles, pagination_size)
    pagination_page = pagination_page if pagination_page <= pag.num_pages else 1
    try:
        exportfiles_page = pag.page(pagination_page)
    except paginator.EmptyPage:
        exportfiles_page = [] # If page is out of range, return empty list.
    #
    number_of_rows = len(exportfiles)
    first_row = (pagination_page - 1) * pagination_size + 1
    last_row = first_row + pagination_size - 1
    last_row = last_row if last_row <= number_of_rows else number_of_rows
    row_info = u"Row " + str(first_row) + " - " + str(last_row) + " of " + str(number_of_rows) 
    prev_page = pagination_page - 1 if pagination_page > 1 else pagination_page
    next_page = pagination_page + 1 if pagination_page < pag.num_pages else pagination_page

    return render(request, "list_exportfiles.html",
                              {'row_info' : row_info, 
                               'page' : pagination_page,
                               'per_page' : pagination_size,
                               'prev_page' :  prev_page,
                               'next_page' : next_page,
                               'pages' : pag.num_pages,
                               'formats' : format_list,
                               'selected_format' : selected_format,
                               'exportfiles' : exportfiles_page})
    
def listExportFilesJson(request):
    """ Generates a JSON file containing a list of exportfiles and their properties. """
#     data_header = exportformat_utils.ExportFileUtils().getExportFileListHeaders()
    data_header = [
        'format', 
        'datatype', 
        'year', 
        'status', 
        'approved', 
        'export_name', 
        'export_file_name', 
        'generated_datetime', 
        ]
    #
    exportfiles_json = []
    #
    data_rows = models.ExportFiles.objects.values_list(*data_header)
    for data_row in data_rows:
        row_dict = dict(zip(data_header, map(str, data_row)))
        exportfiles_json.append(row_dict)
    #
#     response = HttpResponse(content_type = 'application/json; charset=cp1252')
    response = HttpResponse(content_type = 'application/json; charset=utf8')
    response['Content-Disposition'] = 'attachment; filename=sharkdata_exportfile_list.json'    
    response.write(json.dumps(exportfiles_json, encoding = 'utf8'))
    return response

def tableExportFilesText(request):
    """ Generates a text file containing a list of exportfiles and their properties. """
#     header_language = request.GET.get('header_language', None)
#     data_header = exportformat_utils.ExportFileUtils().getExportFileListHeaders()
    data_header = [
        'format', 
        'datatype', 
        'year', 
        'status', 
        'approved', 
        'export_name', 
        'export_file_name', 
        'generated_datetime', 
        ]
#     translated_header = exportformat_utils.ExportFileUtils().translateExportFileListHeaders(data_header, 
#                                                                                  language = header_language)
    translated_header = data_header
    #
    data_rows = models.ExportFiles.objects.values_list(*data_header)
    #
    response = HttpResponse(content_type = 'text/plain; charset=cp1252')    
    response['Content-Disposition'] = 'attachment; filename=sharkdata_exportfiles.txt'    
    response.write('\t'.join(translated_header) + '\r\n') # Tab separated.
    for row in data_rows:
        response.write('\t'.join(map(str, row)) + '\r\n') # Tab separated.        
    return response

def tableExportFilesJson(request):
    """ Generates a text file containing a list of exportfiles and their properties. 
        Organised as header and rows.
    """
#     data_header = exportformat_utils.ExportFileUtils().getExportFileListHeaders()
    data_header = [
        'format', 
        'datatype', 
        'year', 
        'status', 
        'approved', 
        'export_name', 
        'export_file_name', 
        'generated_datetime', 
        ]
    #
    data_rows = models.ExportFiles.objects.values_list(*data_header)
    #
    response = HttpResponse(content_type = 'application/json; charset=cp1252')
    response['Content-Disposition'] = 'attachment; filename=sharkdata_exportfiles.json'    
    response.write('{')
    response.write('"header": ["')
    response.write('", "'.join(data_header) + '"], ') # Tab separated.
    response.write('"rows": [')
    row_delimiter = ''
    for row in data_rows:
        response.write(row_delimiter + '["' + '", "'.join(map(str, row)) + '"]')      
        row_delimiter = ', '
    response.write(']')
    response.write('}')
    #
    return response

def deleteExportFile(request, export_name):
    """ Deletes one row in the database. """
    exportfile = models.ExportFiles.objects.get(export_name = export_name)
    #
    if request.method == "GET":
        form = forms.DeleteExportFileForm()
        contextinstance = {'form'   : form,
                           'exportfile' : exportfile,
                           'error_message' : None}
        contextinstance.update(csrf(request))
        return render(request, "delete_exportfile.html", contextinstance)
    elif request.method == "POST":
        error_message = None # initially.
        #
        form = forms.DeleteExportFileForm(request.POST)
        if form.is_valid():
            #
            user = request.POST['user']
            password = request.POST['password']
            if password != settings.APPS_VALID_USERS_AND_PASSWORDS.get(user, None):
                error_message = 'Not a valid user or password. Please try again...'   
            #
            if error_message == None:
                logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Delete export', user=user)
                try:
                    exportfile = models.ExportFiles.objects.get(export_name = export_name)
                    exportfile.delete()
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, 
                                                                   log_row='Export deleted: ' + export_name)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
                except:
                    error_message = u"Can't delete exportfile: " + export_name 
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
            
            if error_message == None:
                return HttpResponseRedirect("/exportformats")
        #
        contextinstance = {'form'   : form,
                           'exportfile' : exportfile,
                           'error_message' : error_message}
        contextinstance.update(csrf(request))
        return render(request, "delete_exportfile.html", contextinstance)
    # Not a valid request method.
    return HttpResponseRedirect("/exportformats")
