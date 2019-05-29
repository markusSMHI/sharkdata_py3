#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import datetime
import hashlib
import app_speciesobs.models as speciesobs_models
import app_datasets.models as datasets_models
import app_exportformats.models as exportformats_models
import sharkdata_core.resources_utils as resources_utils

from django.conf import settings

import sharkdata_core

@sharkdata_core.singleton
class SpeciesObsUtils(object):
    """ Singleton class. """
    def __init__(self):
        """ """
        self._data_header = None
        self._translations = None
        self._header_cleanup = None
        self._update_obs_thread = None
        self._load_obs_thread = None
        self._cleanup_obs_thread = None
        # To avoid duplicates.
        self.observation_id_lookup = []
        # Load resource file containing WoRMS info for taxa.
        self.worms_info_object = sharkdata_core.SpeciesWormsInfo()
        self.worms_info_object.loadSpeciesFromResource()
        #
        self._export_dir_path = pathlib.Path(settings.SHARKDATA_DATA, 'exports')
    
    def getHeaders(self):
        """ """
        if not self._data_header:
            self._data_header = [
                    'occurrence_id',
                    #
                    'data_type', 
                    'scientific_name', 
                    'scientific_authority', 
                    'latitude_dd', 
                    'longitude_dd', 
                    'sampling_date', 
                    'sampling_year', 
                    'sampling_month', 
                    'sampling_day', 
                    'sample_min_depth', 
                    'sample_max_depth', 
                    'sampler_type', 
                    'dyntaxa_id', 
                    'taxon_kingdom', 
                    'taxon_phylum', 
                    'taxon_class', 
                    'taxon_order', 
                    'taxon_family', 
                    'taxon_genus', 
                    'taxon_species', 
                    'orderer', 
                    'reporting_institute', 
                    'sampling_laboratory', 
                    'analytical_laboratory',                     
                    'dataset_name',
                    'dataset_file_name',
                    #
                    'status', # Used by SLU.
#                     'last_update_date', # Used for internal purposes, may be external in the future.
#                     'last_status_change_date', # Not used now, but can be used in the future.
                    ]
        #
        return self._data_header

    def translateHeaders(self, data_header, 
                         resource_name = 'translate_speciesobs_headers', 
                         language = 'darwin_core'):
        """ """
        return resources_utils.ResourcesUtils().translateHeaders(data_header, resource_name, language)
           
    def cleanUpHeader(self, data_header):
        """ Internal columns names from SHARKweb etc. are not stable yet. Replace old style with better style. """
        new_header = []
        #
        if not self._header_cleanup:
            self._header_cleanup = {
                    'datatype': 'data_type', 
                    'scientific_name': 'scientific_name', 
                    'scientific_authority': 'scientific_authority', 
                    'sample_latitude_dd': 'latitude_dd', 
                    'sample_longitude_dd': 'longitude_dd', 
                    'sample_date': 'sampling_date', 
                    'visit_year': 'sampling_year', 
                    'visit_month': 'sampling_month', 
                    'visit_day': 'sampling_day', 
                    'sample_min_depth_m': 'sample_min_depth', 
                    'sample_max_depth_m': 'sample_max_depth', 
                    'sampler_type_code': 'sampler_type', 
                    'variable.taxon_id': 'dyntaxa_id', 
                    'dyntaxa_id': 'dyntaxa_id', 
                    'taxon_kingdom': 'taxon_kingdom', 
                    'taxon_phylum': 'taxon_phylum', 
                    'taxon_class': 'taxon_class', 
                    'taxon_order': 'taxon_order', 
                    'taxon_family': 'taxon_family', 
                    'taxon_genus': 'taxon_genus', 
                    'taxon_species': 'taxon_species', 
                    'orderer_code': 'orderer', 
                    'reporting_institute_code': 'reporting_institute', 
                    'sampling_laboratory_code': 'sampling_laboratory', 
                    'analytical_laboratory_code': 'analytical_laboratory',   
                }            
        #
        for item in data_header:
            if item in self._header_cleanup:
                new_header.append(self._header_cleanup[item])                
            else:
                new_header.append(item)
        #
        return new_header

    def generateSpeciesObs(self, logfile_name, user):
        """ """
        print('Species observations update. Started.')
        
        self.getHeaders()
        
        try:
            
            # Loop over all datasets.
            valid_datatypes = [
                                'Epibenthos', 
                                'GreySeal', 
                                'HarbourSeal', 
                                'Phytoplankton', 
                                'RingedSeal',
                                'Zoobenthos', 
                                'Zooplankton', 
                               ]
            
            for valid_datatype in valid_datatypes:
                # 
                export_name = 'SpeciesObs_SMHI_' + valid_datatype
                export_file_name = export_name + '.txt'
                export_file_path = pathlib.Path(self._export_dir_path, export_file_name)
                error_log_file = export_name + '_log.txt'
                error_log_file_path = pathlib.Path(self._export_dir_path, error_log_file)
                #
                if not export_file_path.parent.exists():
                    export_file_path.parent.mkdir(parents=True)                
                # To avoid duplicates.
                self.observation_id_lookup = []
                # Counters.
                self.counter_rows = 0
                self.counter_duplicates = 0
                #first and last year.
                self.year_min = ''
                self.year_max = ''
                
                with export_file_path.open('w') as obsfile:
                    
                    data_header = self.translateHeaders(self._data_header)
                    obsfile.write('\t'.join(data_header) + '\n')
#                     obsfile.write('\t'.join(self._data_header) + '\n')
                
                    for dataset_queryset in datasets_models.Datasets.objects.all().filter(datatype = valid_datatype).order_by('dataset_name'):
                        self.extract_observations_from_dataset(logfile_name, obsfile, dataset_queryset)
                        
                print('')
                print('Summary for datatype: ', valid_datatype)
                print('- rows: ',  self.counter_rows)
                print('- duplicates', self.counter_duplicates)
                print('')
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='')
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='Summary for datatype: ' + valid_datatype)
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='- file: : ' + export_name)
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='- rows: : ' + str(self.counter_rows))
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='- duplicates: ' + str(self.counter_duplicates))
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='')
                
                # Update database.
                # Delete row if exists.
                export_db_rows = exportformats_models.ExportFiles.objects.filter(export_name = export_name)
                for db_row in export_db_rows: 
                    db_row.delete()
                # Add row.
                years = self.year_min
                if self.year_min and self.year_max:
                    years = self.year_min + '-' + self.year_max
                
                export_db_row = exportformats_models.ExportFiles(
                                format = 'Species-obs',
                                datatype = valid_datatype,
                                year = years,
                                approved = 'True',
                                status = 'ok',
                                export_name = export_name,
                                export_file_name = export_file_name,
                                export_file_path = str(export_file_path),
                                error_log_file = error_log_file,
                                error_log_file_path = error_log_file_path,
                                generated_by = user,
                              )
                export_db_row.save()                
            #           
            sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FINISHED')            #
            print('Species observations update. Finished.')
        #
        except Exception as e:
            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='- Failed. Exception: ' + str(e))
            sharkdata_core.SharkdataAdminUtils().log_close(logfile_name, new_status='FAILED')
                        
    def extract_observations_from_dataset(self, logfile_name, obsfile, dataset_queryset):
        """ """
        print('- ' + dataset_queryset.dataset_file_name)
                        
        sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='Extracting species observations from: ' + dataset_queryset.dataset_file_name + '...')
        
        zipreader = sharkdata_core.SharkArchiveFileReader(dataset_queryset.ftp_file_path)
        try:
            zipreader.open()
            data = zipreader.getDataAsText()
        finally:
            zipreader.close()                        
        #
        encoding = 'cp1252'
        rowseparator = '\n'
        fieldseparator = '\t'
        #
        data = str(data, encoding, 'strict')
        datarows = (item.strip() for item in data.split(rowseparator)) # Generator instead of list.
        #
        for rowindex, datarow in enumerate(datarows):
            #
            try:
                if len(datarow) == 0:
                    continue
                #  
                row = [item.strip() for item in datarow.split(fieldseparator)]
                if rowindex == 0:
                    header = row
                else:
                    header = self.cleanUpHeader(header)
                    rowdict = dict(zip(header, row))
                    
                    rowdict['data_type'] = dataset_queryset.datatype
                    
                    # Scientific name is mandatory.
                    if not rowdict.get('scientific_name', ''):
                        continue
                    
                    # Position. Check if position is valid. Skip row if not.
                    lat_dd = rowdict.get('sample_latitude_dd', '').replace(',', '.')
                    long_dd = rowdict.get('sample_longitude_dd', '').replace(',', '.')
                    if (not lat_dd) or (not long_dd):
                        lat_dd = rowdict.get('latitude_dd', '').replace(',', '.')
                        long_dd = rowdict.get('longitude_dd', '').replace(',', '.')
                    #
                    try:
                        if (float(lat_dd) > 70.0) or (float(lat_dd) < 50.0) or (float(long_dd) > 30.0) or (float(long_dd) < 5.0):
                            sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='Row skipped, position outside box. Latitude: ' + lat_dd + ' Longitude: ' + long_dd + ' Row: ' + str(rowindex))
                            lat_dd = ''
                            long_dd = ''
                    except:
                        lat_dd = ''
                        long_dd = ''
                    #
                    if lat_dd and long_dd:
                        rowdict['latitude_dd'] = lat_dd
                        rowdict['longitude_dd'] = long_dd
                    else:
                        # Don't add to SpeciesObs if position is invalid.
                        continue 
                    #
                    # Calculate DarwinCore Observation Id.
                    generated_occurrence_id = self.calculateDarwinCoreObservationIdAsMD5(rowdict)
                    
                    if generated_occurrence_id not in self.observation_id_lookup:
                        self.observation_id_lookup.append(generated_occurrence_id)                    

                        # Row id as md5.
                        rowdict['occurrence_id'] = generated_occurrence_id

                        # When.
                        tmp_date = rowdict.get('sampling_date', '')
                        if len(tmp_date) >= 10:
                            year = tmp_date[0:4]
                            rowdict['sampling_year'] = year
                            rowdict['sampling_month'] = tmp_date[5:7]
                            rowdict['sampling_day'] = tmp_date[8:10]
                            
                            if (self.year_min == '') or (year < self.year_min):
                                self.year_min = year
                            if (self.year_max == '') or (year > self.year_max):
                                self.year_max = year
                            
                        if not rowdict.get('sample_min_depth', ''):
                            rowdict['sample_min_depth'] = rowdict.get('water_depth_m', '')
                        if not rowdict.get('sample_max_depth', ''):
                            rowdict['sample_max_depth'] = rowdict.get('water_depth_m', '')

                        
                        # Classification.    
                        scientificname = rowdict.get('scientific_name', '-') if rowdict.get('scientific_name') else '-'
                        taxon_worms_info = self.worms_info_object.getTaxonInfoDict(scientificname)
                        if taxon_worms_info:
                            rowdict['taxon_kingdom'] = taxon_worms_info.get('kingdom', '-') if taxon_worms_info.get('kingdom') else '-'
                            rowdict['taxon_phylum'] = taxon_worms_info.get('phylum', '-') if taxon_worms_info.get('phylum') else '-'
                            rowdict['taxon_class'] = taxon_worms_info.get('class', '-') if taxon_worms_info.get('class') else '-'
                            rowdict['taxon_order'] = taxon_worms_info.get('order', '-') if taxon_worms_info.get('order') else '-'
                            rowdict['taxon_family'] = taxon_worms_info.get('family', '-') if taxon_worms_info.get('family') else '-'
                            rowdict['taxon_genus'] = taxon_worms_info.get('genus', '-') if taxon_worms_info.get('genus') else '-'
                        else:
                            rowdict['taxon_kingdom'] = '-'
                            rowdict['taxon_phylum'] = '-'
                            rowdict['taxon_class'] = '-'
                            rowdict['taxon_order'] = '-'
                            rowdict['taxon_family'] = '-'
                            rowdict['taxon_genus'] = '-'
                        #
#                         if not rowdict.get('orderer', ''):
#                             rowdict['orderer'] = rowdict.get('orderer_code', '')
#                         if not rowdict.get('orderer', ''):
#                             rowdict['orderer'] = rowdict.get('sample_orderer_code', '')
#                         if not rowdict.get('orderer', ''):
#                             rowdict['orderer'] = rowdict.get('sample_orderer_name_sv', '')
#                         if not rowdict.get('orderer', ''):
#                             rowdict['orderer'] = rowdict.get('sample_orderer_name_en', '')
#                         if not rowdict.get('reporting_institute', ''):
#                             rowdict['reporting_institute'] = rowdict.get('reporting_institute_code', '')
#                         if not rowdict.get('reporting_institute', ''):
#                             rowdict['reporting_institute'] = rowdict.get('reporting_institute_name_sv', '')
#                         if not rowdict.get('reporting_institute', ''):
#                             rowdict['reporting_institute'] = rowdict.get('reporting_institute_name_en', '')
#                         if not rowdict.get('sampling_laboratory', ''):
#                             rowdict['sampling_laboratory'] = rowdict.get('sampling_laboratory_code', '')
#                         if not rowdict.get('sampling_laboratory', ''):
#                             rowdict['sampling_laboratory'] = rowdict.get('sampling_laboratory_name_sv', '')
#                         if not rowdict.get('sampling_laboratory', ''):
#                             rowdict['sampling_laboratory'] = rowdict.get('sampling_laboratory_name_en', '')
#                         if not rowdict.get('analytical_laboratory', ''):
#                             rowdict['analytical_laboratory'] = rowdict.get('analytical_laboratory_code', '')
#                         if not rowdict.get('analytical_laboratory', ''):
#                             rowdict['analytical_laboratory'] = rowdict.get('analytical_laboratory_name_sv', '')
#                         if not rowdict.get('analytical_laboratory', ''):
#                             rowdict['analytical_laboratory'] = rowdict.get('analytical_laboratory_name_en', '')
                        #
                        out_row = []
                        for header_item in self.getHeaders():
                            out_row.append(rowdict.get(header_item, '-'))
                        #    
                        obsfile.write('\t'.join(out_row) + '\n')
                        self.counter_rows += 1
                    else:
                        #print('- Duplicate md5.')
                        self.counter_duplicates += 1
                    
            except Exception as e:
                sharkdata_core.SharkdataAdminUtils().log_write(logfile_name, log_row='- Error in row ' + str(rowindex) + ': ' + str(e))
    
    def deleteSpeciesObs(self, logfile_name, user):
        """ """
        # Delete from db.
        export_db_rows = exportformats_models.ExportFiles.objects.filter(format='Species-obs')
        for db_row in export_db_rows: 
            db_row.delete()

        # Delete files.
        for file_name in list(self._export_dir_path.glob('SpeciesObs_SMHI_*')):
            file_path = pathlib.Path(file_name)
            if file_path.exists():                
                file_path.unlink()
         
    def calculateDarwinCoreObservationIdAsMD5(self, rowdict):
        """ Calculates DarwinCore Observation Id. It is based on fields that makes the observation unique
            and a MD5 hash value is calculated based on that unique content.
            This strategy is useful because an observation id does no exists in our datasets and this will work
            when the same data is imported multiple times by producing the same id. It will also work if
            the observation is resubmitted in another dataset or with other corrections made to aditional data.  
        """
        tmp_id = rowdict.get('data_type', '') + '+' + \
                 rowdict.get('sampling_date', '') + '+' + \
                 rowdict.get('latitude_dd', '') + '+' + \
                 rowdict.get('longitude_dd', '') + '+' + \
                 rowdict.get('scientific_name', '') + '+' + \
                 rowdict.get('sample_min_depth', '') + '+' + \
                 rowdict.get('sample_max_depth', '') + '+' + \
                 rowdict.get('sampler_type', '')
        # Generates MD5 string of 32 hex digits.
        md5_id = 'MD5 not calculated'
        try:
            md5_id = hashlib.md5(tmp_id.encode('utf-8')).hexdigest()
        except Exception as e:
            md5_id = 'ERROR in MD5 generation.'
            print('Exception: ERROR in MD5 generation: ', e )
        #
        return md5_id

    def isFloat(self, value):
        """ Useful utility. """
        try:
            float(value)
            return True
        except ValueError:
            pass
        return False     
    
