#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
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
        self._metadata_update_thread = None
        self._generate_archives_thread = None
        self._update_obs_thread = None
        self._cleanup_obs_thread = None
        self._load_obs_thread = None
        self._update_obs_thread = None
        self._generate_ices_xml_thread = None
        self._validate_ices_xml_thread = None
        self._generate_dwca_thread = None
        # Path to log files for threaded work.
        self._logfile_dir_path = pathlib.Path(settings.SHARKDATA_DATA, 'admin_log')
    
    def log_create(self, command, user):
        """ """
        starttime = str(datetime.datetime.now()).replace(':', '')[:17]
        logfile_name = starttime + '_' + command + '_RUNNING.txt' 
        logfile_name = logfile_name.replace(' ', '_')
        self._logfile_path = pathlib.Path(self._logfile_dir_path, logfile_name)
        
        if not self._logfile_path.parent.exists():
            self._logfile_path.parent.mkdir(parents=True)
        
        with self._logfile_path.open('w') as logfile:
            logfile.write('\n')
            logfile.write('command: ' + command + '\n')
            logfile.write('started_at: ' + starttime + '\n')
            logfile.write('user: ' + user + '\n')
            logfile.write('\n')
        
        return logfile_name
    
    def log_write(self, logfile_name, log_row):
        """ """
        self._logfile_path = pathlib.Path(self._logfile_dir_path, logfile_name)
        if self._logfile_path.exists():
            with self._logfile_path.open('a') as logfile:
                logfile.write(log_row + '\n')
    
    def log_close(self, logfile_name, new_status):
        """ """
        self._logfile_path = pathlib.Path(self._logfile_dir_path, logfile_name)
        endtime = str(datetime.datetime.now()).replace(':', '').replace(' ', '_')[:17]
        if self._logfile_path.exists():
            with self._logfile_path.open('a') as logfile:
                logfile.write('\n')
                logfile.write('status: ' + new_status + '\n')
                logfile.write('finished_at: ' + endtime + '\n')
                logfile.write('\n')
        
            new_file_name = logfile_name.replace('_RUNNING', '_' + new_status.upper())
            new_path = pathlib.Path(self._logfile_dir_path, new_file_name)
            self._logfile_path.rename(new_path)
    
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
    
    ##### Datasets #####
    
    # TODO: Not in thread yet.
    
    ##### Archives #####
    
#     def generateArchivesForAllDatasetsInThread(self, user):
#         """ """
#         
#         logrow_id = admin_models.createLogRow(command = 'Generate archives (DwC, etc.)', status = 'RUNNING', user = user)
#         try:
#             # Check if generate_archives thread is running.
#             if self._generate_archives_thread:
#                 if self._generate_archives_thread.is_alive():
#                     error_message = u"Generate archives is already running. Please try again later."
#                     admin_models.changeLogRowStatus(logrow_id, status = 'FAILED')
#                     admin_models.addResultLog(logrow_id, result_log = error_message)
#                     #
#                     return
#             # Use a thread to relese the user. This will take some time.
#             self._generate_archives_thread = threading.Thread(target = self.generateArchivesForAllDatasets, args=(logrow_id, user, ))
#             self._generate_archives_thread.start()
#         except:
#             error_message = u"Can't generate_archives."
#             admin_models.changeLogRowStatus(logrow_id, status = 'FAILED')
#             admin_models.addResultLog(logrow_id, result_log = error_message)
#         #
#         return None # No error message.
                
#     def generateArchivesForAllDatasets(self, logrow_id, user):
#         """ """
#         sharkdata_core.ArchiveManager().generateArchivesForAllDatasets(logrow_id, user)

    ##### SpeciesObs #####
    
    def updateSpeciesObsInThread(self, log_row_id):
        """ """
        # Check if update thread is running.
        if self._update_obs_thread:
            if self._update_obs_thread.is_alive():
                return u"Update is already running. Please try again later."
        # Check if load thread is running.
        if self._load_obs_thread:
            if self._load_obs_thread.is_alive():
                return u"Load is already running. Please try again later."              
        # Check if clean up thread is running.
        if self._cleanup_obs_thread:
            if self._cleanup_obs_thread.is_alive():
                return u"Clean up is already running. Please try again later."              
        # Use a thread to relese the user. This task will take some time.
        self._update_obs_thread = threading.Thread(target = sharkdata_core.SpeciesObsUtils().updateSpeciesObs, args=(log_row_id,))
        self._update_obs_thread.start()
        #
        return None # No error message.
         
    def cleanUpSpeciesObsInThread(self, log_row_id):
        """ """
        # Check if update thread is running.
        if self._update_obs_thread:
            if self._update_obs_thread.is_alive():
                return u"Update is already running. Please try again later."
        # Check if load thread is running.
        if self._load_obs_thread:
            if self._load_obs_thread.is_alive():
                return u"Load is already running. Please try again later."              
        # Check if clean up thread is running.
        if self._cleanup_obs_thread:
            if self._cleanup_obs_thread.is_alive():
                return u"Clean up is already running. Please try again later."              
        # Use a thread to relese the user. This task will take some time.
        self._cleanup_obs_thread = threading.Thread(target = sharkdata_core.SpeciesObsUtils().cleanUpSpeciesObs, args=(log_row_id,))
        self._cleanup_obs_thread.start()

        return None # No error message.

    ##### ExportFormats, ICES-XML #####
    
    def generateIcesXmlExportFilesInThread(self, datatype_list, year_from, year_to, monitoring_type, user):
        """ """
        logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Generate ICES-XML files', user=user)
        try:
            # Check if thread is running.
            if self._generate_ices_xml_thread:
                if self._generate_ices_xml_thread.is_alive():
                    error_message = u"Generate ICES-XML files is already running. Please try again later."
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
                    #
                    return
            # Use a thread to relese the user. Log file closed in thread.
            self._generate_ices_xml_thread = threading.Thread(target = sharkdata_core.GenerateIcesXmlExportFiles().generateIcesXmlExportFiles, 
                                                              args=(logfile_name, datatype_list, year_from, year_to, monitoring_type, user ))
            self._generate_ices_xml_thread.start()
        except Exception as e:
            error_message = u"Can't generate ICES-XML file." + '\nException: ' + str(e) + '\n'
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
                    error_message = u"Validate ICES-XML file is already running. Please try again later."
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
                    #
                    return
            # Use a thread to relese the user. Log file closed in thread.
            self._validate_ices_xml_thread = threading.Thread(target = sharkdata_core.ValidateIcesXml().validateIcesXml, 
                                                              args=(logfile_name, datatype_list, user ))
            self._validate_ices_xml_thread.start()
        except Exception as e:
            error_message = u"Can't validate ICES-XML file." + '\nException: ' + str(e) + '\n'
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



#         logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Validate ICES-XML file', user=user)
#         try:
#             # Check if thread is running.
#             if self._validate_ices_xml_thread:
#                 if self._validate_ices_xml_thread.is_alive():
#                     error_message = u"Validate ICES-XML file is already running. Please try again later."
#                     sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
#                     sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
#                     #
#                     return
#             # Use a thread to relese the user. Log file closed in thread.
#             self._validate_ices_xml_thread = threading.Thread(target = sharkdata_core.ValidateIcesXml().validateIcesXml, 
#                                                               args=(logfile_name, datatype_list, user ))
#             self._validate_ices_xml_thread.start()
#         except Exception as e:
#             error_message = u"Can't validate ICES-XML file." + '\nException: ' + str(e) + '\n'
#             sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
#             sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
#         #
        return None # No error message.
                 
    ##### ExportFormats, DwC-A #####
    
    def generateDwcaExportFilesInThread(self, datatype_list, year_from, year_to, status, user):
        """ """
        logfile_name = sharkdata_core.SharkdataAdminUtils().log_create(command='Generate DwC-A files', user=user)
        try:
            # Check if thread is running.
            if self._generate_dwca_thread:
                if self._generate_dwca_thread.is_alive():
                    error_message = u"Generate DwC-A files is already running. Please try again later."
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
                    sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
                    #
                    return
            # Use a thread to relese the user. Log file closed in thread.
            self._generate_dwca_thread = threading.Thread(target = sharkdata_core.GenerateDwcaExportFiles().generateDwcaExportFiles, 
                                                              args=(logfile_name, datatype_list, year_from, year_to, status, user ))
            self._generate_dwca_thread.start()
        except Exception as e:
            error_message = u"Can't generate DwC-A files." + '\nException: ' + str(e) + '\n'
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row=error_message)
            sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
        #
        return None # No error message.
                 
