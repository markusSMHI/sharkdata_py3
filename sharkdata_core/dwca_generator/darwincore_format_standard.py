#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-present SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import datetime
import pathlib
import copy
import pandas as pd

from . import darwincore_utils  
from . import darwincore_meta_xml
from . import darwincore_eml_xml

class DarwinCoreFormatStandard(object):
    """ """
    def __init__(self):
        """ Darwin Core Archive Format base class. """
        self.worms_info_object = None
        #
        self.dwca_event_columns = []
        self.dwca_occurrence_columns = []
        self.dwca_measurementorfact_columns = []
        self.mof_extra_params = None
        #
        self._taxa_lookup_dict = {}
        #
        self.clear()
    
    def clear(self):
        """ """
        self.target_rows = []
        self.dwca_event = [] 
        self.dwca_occurrence = [] 
        self.dwca_measurementorfact = [] 
        #
        self.meta_file_name = None
        self.eml_file_name = None
    
    def prepare_rows(self, dataset_df, dwca_datatype_object):
        """ """
        self.target_rows = []
        # Iterate over rows in dataframe.
        for df_row_dict in dataset_df.to_dict(orient='records'):
            # Copy field not empty.
            row_dict = {}
            for df_key, df_value in df_row_dict.iteritems():
                if str(df_value):
#                     row_dict[df_key] = df_value.strip()
                    row_dict[df_key] = str(df_value).strip()
            # Direct field mapping.
            try:
                for dwc_key, shark_key in dwca_datatype_object.get_default_mapping().iteritems():
                    value = str(row_dict.get(shark_key, ''))
                    if value:
                        row_dict[dwc_key] = value
            except:
                print('DEBUG 1')
                raise
            # More fields.
            try:
                dwca_datatype_object.add_extra_fields(row_dict)
            except:
                print('DEBUG 2')
                raise
            # More keys.
            try:
                dwca_datatype_object.create_extra_keys(row_dict)
            except:
                print('DEBUG 3')
                raise
            # 
            self.target_rows.append(row_dict)
    
    def create_dwca_parts(self, dwca_datatype_object):
        """ Template method. Check http://en.wikipedia.org/wiki/Template_method_pattern """
        print('DEBUG: create_dwca_parts()')
#         print('DEBUG: create_part_event()')
        self.create_dwca_event(dwca_datatype_object)
#         print('DEBUG: create_part_occurrence()')
        self.create_dwca_occurrence(dwca_datatype_object)
#         print('DEBUG: create_part_measurementorfact()')
        self.create_dwca_measurementorfact(dwca_datatype_object)
#         print('DEBUG: create_dwca_parts done.')
    
    def create_dwca_event(self, dwca_datatype_object):
        """ """
        used_visit_event_key_list = []
        used_sample_event_key_list = []
        #
        for target_row in self.target_rows:
            #
            if target_row.get('remove_row', '') == '<REMOVE>':
                continue
            
            # Get keys.
            dwca_visit_id = target_row.get('dwca_visit_id', '')
            dwca_sample_id = target_row.get('dwca_sample_id', '')
            
            dwca_visit_id_short = target_row.get('dwca_visit_id_short', '')
            dwca_sample_id_short = target_row.get('dwca_sample_id_short', '')
            
            # Visit event.
            if dwca_visit_id and (dwca_visit_id not in used_visit_event_key_list):
                used_visit_event_key_list.append(dwca_visit_id)
                #
                event_dict = {}
                for column_name in ['eventDate', 'verbatimLocality', 'decimalLatitude', 'decimalLongitude',
                                    'institutionCode', 'datasetName']:
                    event_dict[column_name] = target_row.get(column_name, '')
                #
                event_dict['type'] = 'Sampling event'
                event_dict['id'] = dwca_visit_id_short
                event_dict['eventID'] = dwca_visit_id_short
                event_dict['parentEventID'] = ''
#                 # Add key to dynamicProperties.
#                 event_dict['dynamicProperties'] = dwca_visit_id
                #
                self.dwca_event.append(event_dict) 
            
            # Sample event.
            if dwca_sample_id and (dwca_sample_id not in used_sample_event_key_list):
                used_sample_event_key_list.append(dwca_sample_id)
                
                event_dict = {}
                for column_name in self.get_event_columns():
                    event_dict[column_name] = target_row.get(column_name, '')
                #
                event_dict['type'] = 'Sample'
                event_dict['id'] = dwca_sample_id_short
                event_dict['eventID'] = dwca_sample_id_short
                event_dict['parentEventID'] = dwca_visit_id_short
#                 # Add key to dynamicProperties.
#                 event_dict['dynamicProperties'] = dwca_sample_id
                #
                self.dwca_event.append(event_dict) 
            
    def create_dwca_occurrence(self, dwca_datatype_object):
        """ """
        used_occurrence_key_list = []
        #
        for target_row in self.target_rows:
            #
            if target_row.get('remove_row', '') == '<REMOVE>':
                continue
            #
            scientific_name = target_row.get('scientific_name', '')
            if scientific_name == '':
                continue
            #
            dwca_occurrence_id = target_row.get('dwca_occurrence_id', '')
            dwca_sample_id_short = target_row.get('dwca_sample_id_short', '')
            dwca_occurrence_id_short = target_row.get('dwca_occurrence_id_short', '')
            #
            if dwca_occurrence_id and (dwca_occurrence_id not in used_occurrence_key_list):
                used_occurrence_key_list.append(dwca_occurrence_id)
                #
                if scientific_name in self._taxa_lookup_dict:
                    occurrence_dict = copy.deepcopy(self._taxa_lookup_dict[scientific_name])
                else:
                    taxa_dict = darwincore_utils.TranslateTaxa().get_translated_aphiaid_and_name(scientific_name)
                    # Taxa info.
                    occurrence_dict = {}
                    #
                    dyntaxa_id = taxa_dict.get('dyntaxa_id', '')
                    if dyntaxa_id:
                        occurrence_dict['taxonID'] = 'urn:lsid:dyntaxa.se:Taxon:' + dyntaxa_id
                    else:
                        occurrence_dict['taxonID'] = ''
                    #
                    occurrence_dict['scientificNameID'] = taxa_dict.get('worms_lsid', '')
#                     occurrence_dict['worms_scientific_name'] = taxa_dict.get('worms_scientific_name', '')            
                    occurrence_dict['taxonRank'] = taxa_dict.get('worms_rank', '')
                    occurrence_dict['kingdom'] = taxa_dict.get('worms_kingdom', '')            
                    occurrence_dict['phylum'] = taxa_dict.get('worms_phylum', '')            
                    occurrence_dict['class'] = taxa_dict.get('worms_class', '')            
                    occurrence_dict['order'] = taxa_dict.get('worms_order', '')            
                    occurrence_dict['family'] = taxa_dict.get('worms_family', '')            
                    occurrence_dict['genus'] = taxa_dict.get('worms_genus', '')
                    #
                    self._taxa_lookup_dict[scientific_name] = copy.deepcopy(occurrence_dict)
                                
                # Direct field mapping.
                for column_name in self.get_occurrence_columns():
                    value = str(target_row.get(column_name, ''))
                    if value:
                        occurrence_dict[column_name] = value
                #
                occurrence_dict['id'] = dwca_sample_id_short
                occurrence_dict['eventID'] = dwca_sample_id_short
                occurrence_dict['occurrenceID'] = dwca_occurrence_id_short            
#                 # Add key to dynamicProperties.
#                 occurrence_dict['dynamicProperties'] = dwca_occurrence_id
                #
                self.dwca_occurrence.append(occurrence_dict) 
    
    def create_dwca_measurementorfact(self, dwca_datatype_object):
        """ """
        used_mof_occurrence_key_list = []
        used_extra_params_visit_list = []
        used_extra_params_sample_list = []
        used_extra_params_occurrence_list = []

        generated_parameters_key_list = []
        
        debug_row_number = 0
        
        for target_row in self.target_rows:
            #
            if target_row.get('remove_row', '') == '<REMOVE>':
                continue
            
            # Keys, both for values from enet and from occurrence.
            dwca_visit_id = target_row.get('dwca_visit_id', '')
            dwca_sample_id = target_row.get('dwca_sample_id', '')
            dwca_occurrence_id = target_row.get('dwca_occurrence_id', '')
            dwca_mof_id = target_row.get('dwca_mof_id', '')
            
            dwca_visit_id_short = target_row.get('dwca_visit_id_short', '')
            dwca_sample_id_short = target_row.get('dwca_sample_id_short', '')
            dwca_occurrence_id_short = target_row.get('dwca_occurrence_id_short', '')
            
            # Extra parameters from column values. Visit level.
            if dwca_visit_id and (dwca_visit_id not in used_extra_params_visit_list):
                used_extra_params_visit_list.append(dwca_visit_id)
                
                if self.mof_extra_params is None:
                    self.mof_extra_params = {
                        'wave_height_m': ('Wave height', 'm'),
                        'wav_observation_code': ('Wave observation code', ''),
                        'weather_observation_code': ('Weather observation code', ''),
                        'wave_exposure_fetch': ('Wave exposure fetch', ''),
                        'wind_speed_ms': ('Wind speed', 'm/s'),
                        'wind_direction_code': ('Wind direction code', ''),
                        'water_level_deviation_m': ('Water level deviation', 'M'),
                        'water_depth_m': ('Water depth', 'M'),
                        'secchi_depth_m': ('Secchi depth', 'm'),
                        'cloud_observation_code': ('Cloud observation code', ''),
                        'insolation_air': ('Insolation air', ''),
                        'incubation_radiation': ('Incubation radiation', ''),
                        'air_temperature_wet_degc': ('Air temperature wet', 'degc'),
                        'air_temperature_degc': ('Air temperature', 'degc'),
                        'air_pressure_hpa': ('Air pressure', 'hpa'),
                        'ice_observation_code': ('Ice observation code', ''),
                        # Part of key:
                        'sediment_deposition_code': ('Sediment deposition code', ''),
                    }
                
                for key, (param, unit) in self.mof_extra_params.iteritems(): 
                    value = str(target_row.get(key, ''))
                    if value: 
                        measurementorfact_dict = {} 
                        measurementorfact_dict['id'] = dwca_visit_id_short 
                        measurementorfact_dict['eventID'] = dwca_visit_id_short 
                        measurementorfact_dict['measurementType'] = param 
                        measurementorfact_dict['measurementValue'] = value 
                        measurementorfact_dict['measurementUnit'] = unit 
                        measurementorfact_dict['measurementDeterminedDate'] = target_row.get('sample_date', '') 
                        #
                        self.dwca_measurementorfact.append(measurementorfact_dict) 
                    
            # Connect to event, sample. Compare keys and use short keys.
            event_key = dwca_sample_id_short
            if dwca_visit_id == dwca_sample_id:
                event_key = dwca_visit_id_short
            elif dwca_sample_id == dwca_sample_id:
                event_key = dwca_sample_id_short
            
            # Used if row contains species.
            occurrence_key = dwca_occurrence_id_short
            if dwca_occurrence_id == dwca_sample_id:
                occurrence_key = ''

            if dwca_mof_id and (dwca_mof_id not in used_mof_occurrence_key_list):
                used_mof_occurrence_key_list.append(dwca_mof_id)
            
                parameter = target_row.get('parameter', '')
                value = target_row.get('value', '')
                unit = target_row.get('unit', '')
                if parameter:
                    measurementorfact_dict = {}
                    measurementorfact_dict['id'] = event_key
                    measurementorfact_dict['eventID'] = event_key
                    measurementorfact_dict['occurrenceID'] = occurrence_key
                    measurementorfact_dict['measurementType'] = parameter
                    measurementorfact_dict['measurementValue'] = value
                    measurementorfact_dict['measurementUnit'] = unit                    
                    measurementorfact_dict['measurementAccuracy'] = ''
                    measurementorfact_dict['measurementDeterminedDate'] = target_row.get('analysis_date', '')
                    measurementorfact_dict['measurementDeterminedBy'] = target_row.get('analysed_by', '')
                    measurementorfact_dict['measurementMethod'] = target_row.get('analysis_method_code', '') # TODO: method_reference_code
                    measurementorfact_dict['measurementRemarks'] = target_row.get('variable_comment', '')
                    #
                    self.dwca_measurementorfact.append(measurementorfact_dict)
                    
                    
                    
                    # Add parameter for size_class.
                    size_class = target_row.get('size_class', '')
                    if size_class:
                        if dwca_occurrence_id_short not in generated_parameters_key_list:
                            generated_parameters_key_list.append(dwca_occurrence_id_short)                                   
                            #
                            measurementorfact_dict_2 = copy.deepcopy(measurementorfact_dict)
#                             measurementorfact_dict_2['id'] = self.measurementorfact_seq_no
#                             self.measurementorfact_seq_no += 1
                            #
                            measurementorfact_dict_2['measurementType'] = 'SizeClass(HELCOM-PEG)'
                            measurementorfact_dict_2['measurementValue'] = size_class
                            measurementorfact_dict_2['measurementUnit'] = ''
                            #
                            self.dwca_measurementorfact.append(measurementorfact_dict_2)
                    
                    
            else:
                if debug_row_number < 100:
                    try:
                        print('DEBUG: dwca_mof_id: ' + str(dwca_mof_id))
                    except Exception as e:
                        print('DEBUG Exception: ' + str(e))
                    debug_row_number += 1
                elif debug_row_number == 100:
                    print('DEBUG: MAX LIMIT OF 100 LOG ROWS.')
                    debug_row_number += 1





    def get_rows(self):
        """ """
        # Darwin Core Archive parts.
        event_content = [] 
        occurrence_content = [] 
        measurementorfact_content = []
          
#         # Append headers for Event, Occurrence and Measurementorfact.
#         event_content.append('\t'.join(self.get_event_columns()))
#         occurrence_content.append('\t'.join(self.get_occurrence_columns())) 
#         measurementorfact_content.append('\t'.join(self.get_measurementorfact_columns()))
         
        # Convert from dictionary to row for each item in the list.
        # Event. 
        for row_dict in self.dwca_event:
            row = []
            for column_name in self.get_event_columns():
                row.append(str(row_dict.get(column_name, '')))
#             event_content.append('\t'.join(row))
            event_content.append(row)
        # Occurrence.
        for row_dict in self.dwca_occurrence:
            row = []
            for column_name in self.get_occurrence_columns():
                row.append(str(row_dict.get(column_name, '')))
#             occurrence_content.append('\t'.join(row))
            occurrence_content.append(row)
        # Measurementorfact.
        for row_dict in self.dwca_measurementorfact:
            row = []
            for column_name in self.get_measurementorfact_columns():
                row.append(str(row_dict.get(column_name, '')))
#             measurementorfact_content.append('\t'.join(row))
            measurementorfact_content.append(row)
                 
        return event_content, occurrence_content, measurementorfact_content











    def save_to_archive_file(self, dwca_file_path, eml_template, metadata_dict):
        """ """
        # Darwin Core Archive parts.
        event_content = [] 
        occurrence_content = [] 
        measurementorfact_content = []
          
        # Append headers for Event, Occurrence and Measurementorfact.
        event_content.append('\t'.join(self.get_event_columns()))
        occurrence_content.append('\t'.join(self.get_occurrence_columns())) 
        measurementorfact_content.append('\t'.join(self.get_measurementorfact_columns()))
         
        # Convert from dictionary to row for each item in the list.
        # Event. 
        for row_dict in self.dwca_event:
            row = []
            for column_name in self.get_event_columns():
                row.append(str(row_dict.get(column_name, '')))
            event_content.append('\t'.join(row))
        # Occurrence.
        for row_dict in self.dwca_occurrence:
            row = []
            for column_name in self.get_occurrence_columns():
                row.append(str(row_dict.get(column_name, '')))
            occurrence_content.append('\t'.join(row))
        # Measurementorfact.
        for row_dict in self.dwca_measurementorfact:
            row = []
            for column_name in self.get_measurementorfact_columns():
                row.append(str(row_dict.get(column_name, '')))
            measurementorfact_content.append('\t'.join(row))
                 
        # Create zip archive.
        ziparchive = darwincore_utils.ZipArchive(dwca_file_path)
        if len(event_content) > 1:
            ziparchive.appendZipEntry('event.txt', ('\r\n'.join(event_content).encode('utf-8')))
        if len(occurrence_content) > 1:
            ziparchive.appendZipEntry('occurrence.txt', ('\r\n'.join(occurrence_content).encode('utf-8')))
        if len(measurementorfact_content) > 1:
            ziparchive.appendZipEntry('extendedmeasurementorfact.txt', ('\r\n'.join(measurementorfact_content).encode('utf-8')))
             
        # Add meta.xml files to zip.
        xml_row_list = darwincore_meta_xml.DarwinCoreMetaXml().create_meta_xml(self.get_event_columns(), 
                                                                               self.get_occurrence_columns(), 
                                                                               self.get_measurementorfact_columns(),
                                                                               )
        if len(xml_row_list) > 1:
            ziparchive.appendZipEntry('meta.xml', ('\r\n'.join(xml_row_list).encode('utf-8')))
         
        # Add eml.xml files to zip.
        xml_row_list = darwincore_eml_xml.DarwinCoreEmlXml().create_eml_xml(eml_template)
        if len(xml_row_list) > 1:
             
            for index, xml_row in enumerate(xml_row_list):
                if 'REPLACE-' in xml_row:                    
                    xml_row_list[index] = xml_row_list[index].replace('REPLACE-packageId', 'TODO-PACKAGE-ID')
                    xml_row_list[index] = xml_row_list[index].replace('REPLACE-pubDate', str(datetime.datetime.today().date()))
                    xml_row_list[index] = xml_row_list[index].replace('REPLACE-westBoundingCoordinate',  str(metadata_dict.get('longitude_dd_min', '')))
                    xml_row_list[index] = xml_row_list[index].replace('REPLACE-eastBoundingCoordinate',  str(metadata_dict.get('longitude_dd_max', '')))
                    xml_row_list[index] = xml_row_list[index].replace('REPLACE-northBoundingCoordinate',  str(metadata_dict.get('latitude_dd_max', '')))
                    xml_row_list[index] = xml_row_list[index].replace('REPLACE-southBoundingCoordinate',  str(metadata_dict.get('latitude_dd_min', '')))
                    xml_row_list[index] = xml_row_list[index].replace('REPLACE-beginDate-calendarDate',  str(metadata_dict.get('sample_date_min', '')))
                    xml_row_list[index] = xml_row_list[index].replace('REPLACE-endDate-calendarDate',  str(metadata_dict.get('sample_date_max', '')))
                    xml_row_list[index] = xml_row_list[index].replace('REPLACE-Parameters',  str(metadata_dict.get('parameter_list', '')))
            #
            eml_document = '\r\n'.join(xml_row_list).encode('utf-8')
            ziparchive.appendZipEntry('eml.xml', eml_document)
    
    
    # === UTILS: ===
    
    def create_key_string(self, row_dict, key_columns):
        """ Util: Generates the key for one row. """
        key_string = ''
        try:
            key_list = [str(row_dict.get(item, '')) for item in key_columns]
#             key_string = '+'.join(key_list)
            key_string = ':'.join(key_list)
        except:
            key_string = 'ERROR: Failed to generate key-string'
        # Replace swedish characters.
        key_string = key_string.replace('Å', 'A')
        key_string = key_string.replace('Ä', 'A')
        key_string = key_string.replace('Ö', 'O')
        key_string = key_string.replace('å', 'a')
        key_string = key_string.replace('ä', 'a')
        key_string = key_string.replace('ö', 'o')
        key_string = key_string.replace('µ', 'u')
        #
        return key_string

    def get_event_columns(self):
        """ Implementation of abstract method declared in DwcaDatatypeBase. """
        if not self.dwca_event_columns:
            self.dwca_event_columns = [
                'id', 
                'eventID', 
                'parentEventID', 
                'type', 
                'samplingProtocol', 
                'sampleSizeValue', 
                'sampleSizeUnit', 
                'samplingEffort', 
                'eventDate', 
                'eventTime', 
                'startDayOfYear', 
                'endDayOfYear', 
                'year', 
                'month', 
                'day', 
                'verbatimEventDate', 
                'habitat', 
                'fieldNumber', 
                'fieldNotes', 
                'eventRemarks', 
                'locationID', 
                'country', 
                'countryCode', 
                'county', 
                'municipality', 
                'locality', 
                'verbatimLocality', 
                'waterBody', 
                'verbatimDepth', 
                'minimumDepthInMeters', 
                'maximumDepthInMeters', 
                'decimalLatitude', 
                'decimalLongitude', 
                'geodeticDatum', 
                'license', 
                'rightsHolder', 
                'accessRights', 
                'bibliographicCitation', 
                'references', 
                'institutionID', 
                'datasetID', 
                'institutionCode', 
                'datasetName', 
                'ownerInstitutionCode', 
                'dataGeneralizations', # (ex: aggregerad över storleksklass...)
                'dynamicProperties', 
            ]
        #
        return self.dwca_event_columns
    
    def get_occurrence_columns(self):
        """ Implementation of abstract method declared in DwcaDatatypeBase. """
        if not self.dwca_occurrence_columns:
            self.dwca_occurrence_columns = [
                'id', 
                'eventID', 
                'occurrenceID', 
                'scientificName', 
                'scientificNameAuthorship', 
                'scientificNameID', 
                'taxonID', 
                'identificationQualifier', 
                'sex', 
                'lifeStage', 
#                 'individualCount', 
#                 'organismQuantity', 
#                 'organismQuantityType', 
                'occurrenceStatus', 
                'preparations', 
                'associatedMedia', 
                'associatedReferences', 
                'associatedSequences', 
                'taxonRank', 
                'kingdom', 
                'phylum', 
                'class', 
                'order', 
                'family', 
                'genus', 
                'basisOfRecord', 
                'recordedBy', 
                'occurrenceRemarks',
                'dynamicProperties', 
            ]
        #
        return self.dwca_occurrence_columns
    
    def get_measurementorfact_columns(self):
        """ Implementation of abstract method declared in DwcaDatatypeBase. """
        if not self.dwca_measurementorfact_columns:
            self.dwca_measurementorfact_columns = [
                'id', 
####                'eventID',
#                 'measurementID', 
                'occurrenceID', 
                'measurementType', 
#                 'measurementTypeID', 
                'measurementValue', 
#                 'measurementValueID', 
                'measurementUnit', 
#                 'measurementUnitID', 
                'measurementAccuracy', 
                'measurementDeterminedDate', 
                'measurementDeterminedBy', 
                'measurementMethod', 
                'measurementRemarks', 
            ]
        #
        return self.dwca_measurementorfact_columns

