#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import urllib
import json
import traceback
import codecs
import datetime
from django.conf import settings
import app_exportformats.models as export_models
# import app_sharkdataadmin.models as admin_models
import sharkdata_core

@sharkdata_core.singleton
class ValidateIcesXml(object):
    """ Singleton class. """
    
    def __init__(self):
        """ """
        self._export_dir_path = os.path.join(settings.APP_DATASETS_FTP_PATH, 'exports')
    
    def validateIcesXml(self, logfile_name, datatype_list, user):
        """ """
        error_counter = 0
        #
        db_exports = export_models.ExportFiles.objects.all()
        for db_export in db_exports:
            if db_export.datatype in datatype_list:
                #
                error_counter = self.validateOneIcesXml(logfile_name, error_counter, db_export, user)        
        #
        if error_counter > 0:
            admin_models.changeLogRowStatus(logrow_id, status = 'FINISHED (Errors: ' + str(error_counter) + ')')
        else:
            admin_models.changeLogRowStatus(logrow_id, status = 'FINISHED')
 
        if settings.DEBUG: print('DEBUG: ICES-XML generation FINISHED')    
                
    def validateOneIcesXml(self, logfile_name, error_counter, db_export, user):
        """ 
        Status = Checked by DC     (No DATSU check)      --> Approved = True
        Status = Not checked   --> Status = DATSU-ok     --> Approved = True
        Status = Not checked   --> Status = DATSU-failed --> Approved = False
        Status = Test          --> Status = Test-DATSU-ok     --> Approved = False
        Status = Test          --> Status = Test-DATSU-failed --> Approved = False
        """
        try:
            # Status 'Checked by DC'.
            if (db_export.status == 'Checked by DC'):
                # Don't perform DATSU check.
                db_export.approved = True
                db_export.save()
                self.append_to_log_file(db_export, datsu_response = None)
            
            # Status 'Not checked'.
            elif (db_export.status == 'Not checked'):
#                 url_part_1 = 'http://datsu.ices.dk/DatsuRest/api/ScreenFile/test,sharkdata,se!exportformats!'
                url_part_1 = 'http://datsu.ices.dk/DatsuRest/api/ScreenFile/sharkdata,se!exportformats!'
                url_part_2 = db_export.export_file_name.replace('.', ',')
                url_part_3 = '/shark!smhi,se' # TODO: shark@smhi.se
                url_part_4 = ''
                if ('Epibenthos' in db_export.export_file_name):
                    url_part_4 = '/pb' 
                elif ('Phytoplankton' in db_export.export_file_name):
                    url_part_4 = '/pp' 
                elif ('Zoobenthos' in db_export.export_file_name):
                    url_part_4 = '/zb' 
                elif ('Zooplankton' in db_export.export_file_name):
                    url_part_4 = '/zp' 
                #
                if settings.DEBUG: print(url_part_1 + url_part_2 + url_part_3 + url_part_4)
                #
                datsu_response_json = urllib.request.urlopen(url_part_1 + url_part_2 + url_part_3 + url_part_4)
                datsu_response = json.load(datsu_response_json)
#                 # For test:
#                 datsu_response = dict({u'SessionID': u'484', u'NumberOfErrors': -1, u'ScreenResultURL': u'datsu.ices.dk/test/ScreenResult.aspx?groupError=0&sessionid=484'})            
                #
                if settings.DEBUG: print('DEBUG: \n' + json.dumps(datsu_response, sort_keys = True, indent = 2))
                #
                if datsu_response.get('NumberOfErrors', 0) == -1:
                    db_export.status = 'DATSU-ok'
                    db_export.approved = True
                else:    
                    db_export.status = 'DATSU-failed'
                    db_export.approved = False
                #
                db_export.save()
                self.append_to_log_file(db_export, datsu_response = datsu_response)
            
            # Status 'Test'.
            elif (db_export.status == 'Test'):
                url_part_1 = 'http://datsu.ices.dk/DatsuRest/api/ScreenFile/test,sharkdata,se!exportformats!'
                url_part_2 = db_export.export_file_name.replace('.', ',')
                url_part_3 = '/shark!smhi,se' # TODO: shark@smhi.se
                url_part_4 = '/zb' 
                #
                if settings.DEBUG: print(url_part_1 + url_part_2 + url_part_3 + url_part_4)
                #
                datsu_response_json = urllib.request.urlopen(url_part_1 + url_part_2 + url_part_3 + url_part_4)
                datsu_response = json.load(datsu_response_json)
#                 # For test:
#                 datsu_response = dict({u'SessionID': u'484', u'NumberOfErrors': -1, u'ScreenResultURL': u'datsu.ices.dk/test/ScreenResult.aspx?groupError=0&sessionid=484'})            
                if settings.DEBUG: print('DEBUG: \n' + json.dumps(datsu_response, sort_keys = True, indent = 2))
                #
                if datsu_response.get('NumberOfErrors', 0) == -1:
                    db_export.status = 'Test-DATSU-ok'
                    db_export.approved = False
                else:    
                    db_export.status = 'Test-DATSU-failed'
                    db_export.approved = False
                    # Logging.
#                     admin_models.addResultLog(logrow_id, result_log = 'ERROR: Failed to validating ICES-XML file. DATSU errors URL: ' + datsu_response.get('ScreenResultURL', '<not defined>'))        
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='ERROR: Failed to validating ICES-XML file. DATSU errors URL: ' + datsu_response.get('ScreenResultURL', '<not defined>'))
                #
                db_export.save()
                self.append_to_log_file(db_export, datsu_response = datsu_response)            
            
            else:
                if settings.DEBUG: print('DEBUG: ' + db_export.export_file_name + '   ' + db_export.status + '   ' + str(db_export.approved))    

        except Exception as e:
            error_counter += 1 
            traceback.print_exc()
#             admin_models.addResultLog(logrow_id, result_log = 'ERROR: Failed to validating ICES-XML files. Exception: ' + str(e))   
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='ERROR: Failed to validating ICES-XML files. Exception: ' + str(e))
            
        return error_counter                 
        
    def append_to_log_file(self, db_export, datsu_response = None, encoding = 'cp1252', row_separator = '\r\n'):
        """ """
        outfile = None
        file_path_name = db_export.error_log_file_path
        out_rows = []
        out_rows.append('')
        out_rows.append('Validate ICES-XML files. ' + str(datetime.datetime.now()))
        out_rows.append('')
        out_rows.append('- Status: ' + db_export.status)
        out_rows.append('- Approved: ' + str(db_export.approved))
        out_rows.append('')
        if datsu_response:
            out_rows.append('- DATSU errors: ' + str(datsu_response.get('NumberOfErrors', '<not defined>')))
            out_rows.append('- DATSU results: ' + datsu_response.get('ScreenResultURL', '<not defined>'))
        #
        try:
            outfile = codecs.open(file_path_name, mode = 'a', encoding = encoding)
            for row in out_rows:
                outfile.write(row + row_separator)
        except (IOError, OSError):
            if settings.DEBUG: print("Failed to write log file: " + file_path_name)
#             raise UserWarning("Failed to write log file: " + file_path_name)
        finally:
            if outfile: outfile.close()
        
        

