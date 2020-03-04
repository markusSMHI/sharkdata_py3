#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-present SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
# import zipfile
import datetime
import threading
from django.conf import settings
# import app_datasets.models as datasets_models
# import app_sharkdataadmin.models as admin_models
import sharkdata_core

@sharkdata_core.singleton
class SharkdataAdminUtils(object):
    """ Singleton class. """
    def __init__(self):
        """ """
        self._update_thread = None
        self._generate_ices_xml_thread = None
        self._validate_ices_xml_thread = None
        self._generate_dwca_thread = None
        self._generate_obs_thread = None
        self._delete_obs_thread = None
        # Path to log files for threaded work.
        self._logfile_dir_path = pathlib.Path(settings.SHARKDATA_DATA, 'admin_log')
    
    ##### Log files. #####

    def log_create(self, command, user):
        """ """
        starttime = str(datetime.datetime.now()).replace(':', '')[:17]
        logfile_name = starttime + '_' + command + '_RUNNING.txt' 
        logfile_name = logfile_name.replace(' ', '_')
        logfile_path = pathlib.Path(self._logfile_dir_path, logfile_name)
        
        if not logfile_path.parent.exists():
            logfile_path.parent.mkdir(parents=True)
        
        with logfile_path.open('w') as logfile:
            logfile.write('\n')
            logfile.write('command: ' + command + '\n')
            logfile.write('started_at: ' + starttime + '\n')
            logfile.write('user: ' + user + '\n')
            logfile.write('\n')
        
        return logfile_name
    
    def log_write(self, logfile_name, log_row):
        """ """
        logfile_path = pathlib.Path(self._logfile_dir_path, logfile_name)
        if logfile_path.exists():
            with logfile_path.open('a') as logfile:
                logfile.write(log_row + '\n')
    
    def log_close(self, logfile_name, new_status):
        """ """
        logfile_path = pathlib.Path(self._logfile_dir_path, logfile_name)
        endtime = str(datetime.datetime.now()).replace(':', '').replace(' ', '_')[:17]
        if logfile_path.exists():
            with logfile_path.open('a') as logfile:
                logfile.write('\n')
                logfile.write('status: ' + new_status + '\n')
                logfile.write('finished_at: ' + endtime + '\n')
                logfile.write('\n')
        
            new_file_name = logfile_name.replace('_RUNNING', '_' + new_status.upper())
            new_path = pathlib.Path(self._logfile_dir_path, new_file_name)
            logfile_path.rename(new_path)
    
    def get_log_files(self):
        """ """
        counter = 0
        log_list = []
        if self._logfile_dir_path.exists():
            for file_name in sorted(list(self._logfile_dir_path.glob('*.txt')), reverse=True):
                counter += 1
                if counter <= 100:
                    log_list.append(file_name)
                else: 
                    # Remove old files.
                    file_path = pathlib.Path(file_name)
                    if file_path.exists():
                        file_path.unlink()
                
        return log_list
    
    def get_log_file_content(self, file_stem):
        """ """
        content = ''
        logfile_path = pathlib.Path(self._logfile_dir_path, file_stem + '.txt')
        if logfile_path.exists():
            with logfile_path.open('r') as logfile:
                content = logfile.read()
        else:
            # Check if status changed.
            parts = file_stem.split('_')
            file_stem_without_status = '_'.join(parts[0:-1])
            file_list = list(self._logfile_dir_path.glob(file_stem_without_status + '*.txt'))
            if len(file_list) > 0:
                file_name = file_list[0]
                logfile_path = pathlib.Path(file_name)
                if logfile_path.exists():
                    with logfile_path.open('r') as logfile:
                        content = logfile.read()
                
        return content
    
    ##### Datasets & resources #####
    
    def updateDatasetsAndResourcesInThread(self, user):
        """ """
        logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Update datasets and resources', user=user)
        try:
            # Check if thread is running.
            if self._update_thread:
                if self._update_thread.is_alive():
                    error_message = '"Update datasets and resources" is already running. Please try again later.'
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
                    #
                    return error_message
            # Use a thread to relese the user. Log file closed in thread.
            
            self._update_thread = threading.Thread(target = self.updateDatasetsAndResources, 
                                                              args=(logfile_name, user, ))
            self._update_thread.start()
        except Exception as e:
            error_message = 'Failed when loading datasets or resources.' + '\nException: ' + str(e) + '\n'
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
            sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
        #
        return None # No error message.
                 
    def updateDatasetsAndResources(self, logfile_name, user):
        """ """
        error_counter = 0
        try:
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='\nDatasets:')
            error_counter += sharkdata_core.DatasetUtils().writeLatestDatasetsInfoToDb(logfile_name, )
        
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='\nResources:')
            error_counter += sharkdata_core.ResourcesUtils().writeResourcesInfoToDb(logfile_name, )
        
            if error_counter > 0:
                sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED-' + str(error_counter) + '-errors')
            else:
                sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')
            
        except Exception as e:
            error_message = 'Failed when loading datasets or resources.' + '\nException: ' + str(e) + '\n'
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
            sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
        #
        return None # No error message.
                 
    ##### ExportFormats, ICES-XML #####
    
    def generateIcesXmlExportFilesInThread(self, datatype_list, year_from, year_to, monitoring_type, user):
        """ """
        logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Generate ICES-XML files', user=user)
        try:
            # Check if thread is running.
            if self._generate_ices_xml_thread:
                if self._generate_ices_xml_thread.is_alive():
                    error_message = '"Generate ICES-XML files" is already running. Please try again later.'
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
                    #
                    return error_message
            # Use a thread to relese the user. Log file closed in thread.
            self._generate_ices_xml_thread = threading.Thread(target = sharkdata_core.GenerateIcesXmlExportFiles().generateIcesXmlExportFiles, 
                                                              args=(logfile_name, datatype_list, year_from, year_to, monitoring_type, user ))
            self._generate_ices_xml_thread.start()
        except Exception as e:
            error_message = 'Can\'t generate ICES-XML file.' + '\nException: ' + str(e) + '\n'
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
            sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
        #
        return None # No error message.
                 
    def validateIcesXmlInThread(self, datatype_list, user):
        """ """
        logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Validate ICES-XML file', user=user)
        try:
            # Check if thread is running.
            if self._validate_ices_xml_thread:
                if self._validate_ices_xml_thread.is_alive():
                    error_message = '"Validate ICES-XML files" is already running. Please try again later.'
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
                    #
                    return error_message
            # Use a thread to relese the user. Log file closed in thread.
            self._validate_ices_xml_thread = threading.Thread(target = sharkdata_core.ValidateIcesXml().validateIcesXml, 
                                                              args=(logfile_name, datatype_list, user ))
            self._validate_ices_xml_thread.start()
        except Exception as e:
            error_message = 'Can\'t validate ICES-XML file.' + '\nException: ' + str(e) + '\n'
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
            sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
        #
        return None # No error message.
                 
    def deleteIcesXmlFiles(self, logfile_name):
        """ """
        for file_name in list(self._logfile_dir_path.glob('ICES-XML*')):
            file_path = pathlib.Path(file_name)
            if file_path.exists():                
                file_path.unlink()
                 
    ##### ExportFormats, DwC-A #####
    
    def generateDwcaExportFilesInThread(self, datatype_list, year_from, year_to, status, user):
        """ """
        logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Generate DwC-A files', user=user)
        try:
            # Check if thread is running.
            if self._generate_dwca_thread:
                if self._generate_dwca_thread.is_alive():
                    error_message = '"Generate DwC-A files" is already running. Please try again later.'
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
                    #
                    return error_message
            # Use a thread to relese the user. Log file closed in thread.
            self._generate_dwca_thread = threading.Thread(target = sharkdata_core.GenerateDwcaExportFiles().generateDwcaExportFiles, 
                                                              args=(logfile_name, datatype_list, year_from, year_to, status, user ))
            self._generate_dwca_thread.start()
        except Exception as e:
            error_message = 'Can\'t generate DwC-A files.' + '\nException: ' + str(e) + '\n'
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
            sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
        #
        return None # No error message.
                 
    ##### SpeciesObs #####
    
    def generateSpeciesObsInThread(self, user):
        """ """
        logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Generate species observations', user=user)
        try:
            # Check if thread is running.
            if self._generate_obs_thread:
                if self._generate_obs_thread.is_alive():
                    error_message = '"Generate species observations" is already running. Please try again later.'
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
                    #
                    return error_message
            # Use a thread to relese the user. Log file closed in thread.
            self._generate_obs_thread = threading.Thread(target = sharkdata_core.SpeciesObsUtils().generateSpeciesObs, 
                                                              args=(logfile_name, user, ))
            self._generate_obs_thread.start()
        except Exception as e:
            error_message = 'Can\'t generate species observations.' + '\nException: ' + str(e) + '\n'
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
            sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
        #
        return None # No error message.
             
    def deleteSpeciesObsInThread(self, user):
        """ """
        logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Delete species observations', user=user)
        try:
            # Check if thread is running.
            if self._delete_obs_thread:
                if self._delete_obs_thread.is_alive():
                    error_message = '"Delete species observations" is already running. Please try again later.'
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
                    #
                    return error_message
            # Use a thread to relese the user. Log file closed in thread.
            self._delete_obs_thread = threading.Thread(target = sharkdata_core.SpeciesObsUtils().deleteSpeciesObs, 
                                                              args=(logfile_name, user, ))
            self._delete_obs_thread.start()
        except Exception as e:
            error_message = 'Can\'t delete species observations.' + '\nException: ' + str(e) + '\n'
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
            sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
        #
        return None # No error message.
