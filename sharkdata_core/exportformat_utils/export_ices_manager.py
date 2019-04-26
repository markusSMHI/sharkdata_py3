#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import traceback
import datetime
from django.conf import settings
import sharkdata_core
import app_exportformats.models as export_models
import app_datasets.models as datasets_models
# import app_sharkdataadmin.models as admin_models

@sharkdata_core.singleton
class GenerateIcesXmlExportFiles(object):
    """ Singleton class. """
    
    def __init__(self):
        """ """
        self._ftp_dir_path = os.path.join(settings.APP_DATASETS_FTP_PATH, 'datasets')
        self._export_dir_path = os.path.join(settings.APP_DATASETS_FTP_PATH, 'exports')
        self._translate_taxa = None
    
    def generateIcesXmlExportFiles(self, logfile_name, 
                        datatype_list, year_from, year_to, status, user):
        """ """
        try:
            # Load resource content for ICES station.
            sharkdata_core.ExportStations().load_export_stations('export_ices_stations')
            # Load resource content for filtering reported data.
            sharkdata_core.ExportFilter().load_export_filter('export_ices_filters')
            # Load resource content to translate values.
            sharkdata_core.TranslateValues().load_export_translate_values('export_ices_translate_values')
            # Load resource content to translate from DynTaxa to WoRMS.
            sharkdata_core.TranslateTaxa().load_translate_taxa('translate_dyntaxa_to_worms')
            # Load resource content to translate from DynTaxa to Helcom PEG.
            sharkdata_core.TranslateDyntaxaToHelcomPeg().load_translate_taxa('translate_dyntaxa_to_helcom_peg')
            
            # Create target directory if not exists.
            if not os.path.exists( self._export_dir_path):
                os.makedirs( self._export_dir_path)
            #
            error_counter = 0
            #
            # Iterate over selected datatypes.
            for datatype in datatype_list:
                year_int = int(year_from)
                year_to_int = int(year_to)
                while year_int <= year_to_int:
                    ""
                    self.generateOneIcesXml(logfile_name, error_counter, 
                               datatype, year_int, status, user)
                    #
                    year_int += 1
            #
            if error_counter > 0:
                admin_models.changeLogRowStatus(logrow_id, status = 'FINISHED (Errors: ' + str(error_counter) + ')')
            else:
                admin_models.changeLogRowStatus(logrow_id, status = 'FINISHED')
                
            # Log missing stations.
            missing_station_list = sharkdata_core.ExportStations().get_missing_station_list()
            if len(missing_station_list) > 0:
#                 admin_models.addResultLog(logrow_id, result_log = 'Missing station(s): ')
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='Missing station(s): ')
                for missing_station in sorted(missing_station_list):
#                     admin_models.addResultLog(logrow_id, result_log = '- ' + missing_station)
                    sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='- ' + missing_station)
                    if settings.DEBUG: print('DEBUG: missing station: ' + missing_station)
#                 admin_models.addResultLog(logrow_id, result_log = '')
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='')
                
            # Log missing taxa.
            missing_taxa_list = sharkdata_core.TranslateTaxa().get_missing_taxa_list()
            if len(missing_taxa_list) > 0:
                admin_models.addResultLog(logrow_id, result_log = 'Missing taxa: ')
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
                for missing_taxa in sorted(missing_taxa_list):
                    # Don't log filtered taxa. 
                    if missing_taxa not in sharkdata_core.ExportFilter().get_filter_remove_list('scientific_name'):
                        admin_models.addResultLog(logrow_id, result_log = '- ' + missing_taxa)
                        sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
                        if settings.DEBUG: print('DEBUG: missing taxon: ' + missing_taxa)
                admin_models.addResultLog(logrow_id, result_log = '')
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
            #
            if settings.DEBUG: print('DEBUG: ICES-XML generation FINISHED')
        except Exception as e:
            admin_models.changeLogRowStatus(logrow_id, status = 'FAILED')
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')
            error_message = u"Can't generate ICES-XML file." + '\nException: ' + str(e) + '\n'
            admin_models.addResultLog(logrow_id, result_log = error_message)
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='+++++')

        
    def generateOneIcesXml(self, logfile_name, error_counter, 
                           datatype, year, status, user):
        """ """        
        # Add all rows from all datasets that match datatype and year.
        icesxmlgenerator = sharkdata_core.IcesXmlGenerator()
        #
        db_datasets = datasets_models.Datasets.objects.all()
        for db_dataset in db_datasets:
            if db_dataset.datatype.upper() != datatype.upper():
                continue
            # Check metadata for year(s) in dataset.
            metadata_as_text = db_dataset.content_metadata_auto
            metadata_dict = {}
            for row in metadata_as_text.split('\r\n'):
                if ':' in row:
                    parts = row.split(':', 1) # Split on first occurence.
                    key = parts[0].strip()
                    value = parts[1].strip()
                    metadata_dict[key] = value
            #
            min_year_int = int(metadata_dict.get('min_year', 0))
            max_year_int = int(metadata_dict.get('max_year', 0))
            if (year < min_year_int) or (year > max_year_int):
                continue # Don't use this dataset.
            #
            dataset_name = metadata_dict.get('dataset_name', 0)
            if dataset_name not in sharkdata_core.ExportFilter().get_filter_keep_list('dataset_name'):
                continue # Don't use this dataset.
            #
            try:
                zip_file_name = db_dataset.dataset_file_name
#                 admin_models.addResultLog(logrow_id, result_log = 'Reading archive file: ' + zip_file_name + '...')
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='Reading archive file: ' + zip_file_name + '...')
                if settings.DEBUG:
                    if settings.DEBUG: print('DEBUG: ICES-ZIP processing: ' + zip_file_name)            
                #
                dataset = sharkdata_core.Dataset()
                dataset.loadDataFromZipFile(zip_file_name,
                                            dataset_dir_path = self._ftp_dir_path,
                                            encoding = 'cp1252')
                #
                dataheader = dataset.data_header
                if settings.DEBUG: 
                    print(dataheader)
                #
                
                # Phytobentos or Zoobenthos. Transect data for record 40.
                transect_data = sharkdata_core.TransectData()
                transect_data.clear()
                if (metadata_dict.get('datatype', 'Epibenthos')) or \
                   (metadata_dict.get('datatype', 'Phytobenthos')): # or \
                #   (metadata_dict.get('datatype', 'Zoobenthos')):
                    transect_data.load_all_transect_data(dataset)
                
                # 
                # Process rows.
                for datarow in dataset.data_rows:
                    datarow_dict = dict(zip(dataheader, map(str, datarow)))
                    #
                    if datarow_dict.get('visit_year', '') == str(year):
                        
                        # Remove some projects.
                        proj = datarow_dict.get('sample_project_name_en', '')
                        if not proj:
                            proj = datarow_dict.get('sample_project_name_sv', '')
                        remove_list_sv = sharkdata_core.ExportFilter().get_filter_remove_list('sample_project_name_sv')
                        remove_list_en = sharkdata_core.ExportFilter().get_filter_remove_list('sample_project_name_en')
                        # 
                        if proj in remove_list_sv:
                            continue
                        if proj in remove_list_en:
                            continue
                        
                        # Remove some stations.
                        station_name = datarow_dict.get('station_name', '')
                        if station_name in sharkdata_core.ExportFilter().get_filter_remove_list('station_name'):
                            continue
                        
                        # Remove RAMSKRAP. 
                        if 'FRAMENET' == datarow_dict.get('sampler_type_code', ''):
                            continue
                        
                        
                        # OK to add row.
                        icesxmlgenerator.add_row(datarow_dict)
                            
            #
            except Exception as e:
                error_counter += 1 
                traceback.print_exc()
#                 admin_models.addResultLog(logrow_id, result_log = 'ERROR: Failed to generate ICES-XML from: ' + zip_file_name + '.')                
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='ERROR: Failed to generate ICES-XML from: ' + zip_file_name + '.')
        #
        try:
            # Create and save the result.
            out_rows = icesxmlgenerator.create_xml()
            #          
            if settings.DEBUG: 
                print('DEBUG: ' + str(len(out_rows)))
            #
            if len(out_rows) > 1:
                #
                export_name = 'ICES-XML' + '_SMHI_' + datatype + '_' + str(year)
                export_file_name = export_name + '.xml'
                export_file_path = os.path.join(self._export_dir_path, export_file_name)
                error_log_file = export_name + '_log.txt'
                error_log_file_path = os.path.join(self._export_dir_path, error_log_file)
                #
                icesxmlgenerator.save_xml_file(out_rows, export_file_path)
                # Update database.
                # Delete row if exists.
                export_db_rows = export_models.ExportFiles.objects.filter(export_name = export_name)
                for db_row in export_db_rows: 
                    db_row.delete()
                #
                approved = False
                if status == 'Checked by DC':
                    approved = True # Will not be validated via DATSU.
                    
                # Write row.
                dbrow = export_models.ExportFiles(
                                format = 'ICES-XML',
                                datatype = datatype,
                                year = str(year),
                                approved = approved,
                                status = status,
                                export_name = export_name,
                                export_file_name = export_file_name,
                                export_file_path = export_file_path,
                                error_log_file = error_log_file,
                                error_log_file_path = error_log_file_path,
                                generated_by = user,
                              )
                dbrow.save()
                
                # Log file.
                log_rows = []
                log_rows.append('')
                log_rows.append('')
                log_rows.append('Generate ICES-XML files. ' + str(datetime.datetime.now()))
                log_rows.append('')
                log_rows.append('- Format: ' + dbrow.format)
                log_rows.append('- Datatype: ' + str(dbrow.datatype))
                log_rows.append('- Year: ' + str(dbrow.year))
                log_rows.append('- Status: ' + str(dbrow.status))
                log_rows.append('- Approved: ' + str(dbrow.approved))
                log_rows.append('- Export name: ' + str(dbrow.export_name))
                log_rows.append('- Export file name: ' + str(dbrow.export_file_name))
                log_rows.append('')
                #
                icesxmlgenerator.save_log_file(log_rows, error_log_file_path)
        #
        except Exception as e:
            error_counter += 1 
            traceback.print_exc()
#             admin_models.addResultLog(logrow_id, result_log = 'ERROR: Failed to generate ICES-XML files. Exception: ' + str(e))              
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='ERROR: Failed to generate ICES-XML files. Exception: ' + str(e))

