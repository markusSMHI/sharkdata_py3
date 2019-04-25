#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import hashlib
from . import darwincore_data_base

class DarwinCoreDataRingedSeal(darwincore_data_base.DarwinCoreDataBase):
    """ """
    def __init__(self):
        """ """
        #
        super(DarwinCoreDataRingedSeal, self).__init__()
        #
        self.dwca_default_mapping = []
        self.indata_visit_event_key_columns = []
        self.indata_sample_event_key_columns = []
        self.indata_occurrence_keys = []
        self.indata_measurementorfact_key_columns = []
        
        self.dwca_visit_id_short_names = []
        self.dwca_sample_id_short_names = []
        self.dwca_occurrence_id_short_names = []

    def add_extra_fields(self, row_dict):
        """ Implementation of abstract method declared in DwcaDatatypeBase. """
        

        # Don't use "Calculated # counted".
        if  row_dict.get('parameter', '') == 'Calculated # counted':
            row_dict['remove_row'] = '<REMOVE>'


        row_dict['collection_code'] = 'SHARK RingedSeal'
        row_dict['country'] = 'Sweden'
        row_dict['countryCode'] = 'SE'                

        # RLABO
        labo_list = ['reporting_institute_code', 'reporting_institute_name_en', 'reporting_institute_name_sv', 
                     'sampling_laboratory_code', 'sampling_laboratory_name_en', 'sampling_laboratory_name_sv']
        for labo in labo_list:
            rlabo = row_dict.get(labo, '')
            if rlabo:
                row_dict['institutionCode'] = rlabo
                break
        
        row_dict['basisOfRecord'] = 'HumanObservation'
        
        # occurrenceStatus.
        row_dict['occurrenceStatus'] = 'present'
        try:
            value = row_dict.get('value', '')
            if float(value) == 0.0:
                row_dict['occurrenceStatus'] = 'absent'
                parameter = row_dict.get('parameter', '')
                print('DEBUG: absent:' + parameter)
        except:
            pass
        
        self.generated_parameters = {}
        #
        try:
            sample_date_str = str(row_dict['sample_date'])
#             row_dict['year'] = sample_date_str[0:4]
            row_dict['month'] = sample_date_str[5:7]
            row_dict['day'] = sample_date_str[8:10]
        except:
            pass
                                   
        # Dynamic properties. Used for Size classes in Phytoplancton etc. 
#         self.dynamic_properties_items = {}
#         if len(self.dynamic_properties_items) > 0:
#             dynamic_properties_list = []
#             for key, value in self.dynamic_properties_items.items():
#                 if row_dict.get(value, None):
#                     dynamic_properties_list.append('"' + key + '":"' + str(row_dict.get(value, '')) + '"')
#             if len(dynamic_properties_list) > 0:
#                 row_dict['dynamicProperties'] = '{' + ', '.join(dynamic_properties_list) + '}'                 
           
            
        # Identification Qualifier. Used for species related qualifiers. 
#         self.identification_qualifier_items = {}
#         if len(self.identification_qualifier_items) > 0:
#             identification_qualifier_list = []
#             for key, value in self.identification_qualifier_items.items():
#                 if row_dict.get(value, None):
#                     identification_qualifier_list.append('"' + key + '":"' + str(row_dict.get(value, '')) + '"')
#             if len(identification_qualifier_list) > 0:
#                 row_dict['identificationQualifier'] = '{' + ', '.join(identification_qualifier_list) + '}' 
         
         
        # Field_number. Used for sample_id, sample_part_id, etc. 
        self.field_number_items = ['sample_series', 
                                   'sample_id', 
                                   'sample_part_id'] 
        if len(self.field_number_items) > 0:
            field_number_list = []
            for key in self.field_number_items:
                if row_dict.get(key, None):
                    field_number_list.append(str(row_dict.get(key, '')))
            row_dict['fieldNumber'] = '-'.join(field_number_list)  
                           
        # Time zone info. (+01:00 or +02:00 (DST=Daylight Savings Time) for Sweden. 
        event_date = row_dict.get('eventDate', '')
        event_time = row_dict.get('eventTime', '')
        if (event_time != '') and (event_time != ''):
            if self.is_daylight_savings_time(event_date):
                row_dict['eventTime'] = event_time + '+02:00'
            else:
                row_dict['eventTime'] = event_time + '+01:00'
    
    def create_extra_keys(self, row_dict):
        """ Implementation of abstract method declared in DwcaDatatypeBase. """
        
        try:
            # Visit.
            key_list = [('station', 'station_name'), 
                        ('date', 'sample_date'), 
#                         ('time', 'sample_time'), 
                       ]
            dwca_visit_id = self._create_extra_key(row_dict, key_list)
            row_dict['dwca_visit_id'] = dwca_visit_id
             
            # Used to generate short names.
            if dwca_visit_id not in self.dwca_visit_id_short_names:
                self.dwca_visit_id_short_names.append(dwca_visit_id)
            dwca_visit_id_short = 'SharkRingedseal-EVENT-' + str(self.dwca_visit_id_short_names.index(dwca_visit_id) + 1)
            row_dict['dwca_visit_id_short'] = dwca_visit_id_short
             
            # Sample.
            key_list = [
                        ('shark_sample_id_md5', 'shark_sample_id_md5'), 
                        ('time', 'sample_time'), 
                       ]
            dwca_sample_id = dwca_visit_id
            extra_keys = self._create_extra_key(row_dict, key_list)
            if extra_keys:
                dwca_sample_id += ':' + extra_keys
            row_dict['dwca_sample_id'] = dwca_sample_id
            row_dict['dwca_sample_id_md5'] = hashlib.md5(dwca_sample_id).hexdigest()
             
            # Used to generate short names.
            if dwca_sample_id not in self.dwca_sample_id_short_names:
                self.dwca_sample_id_short_names.append(dwca_sample_id)
            dwca_sample_id_short =  dwca_visit_id_short + ':' + 'SAMPLE-' + str(self.dwca_sample_id_short_names.index(dwca_sample_id) + 1)
            row_dict['dwca_sample_id_short'] = dwca_sample_id_short
     
     
            # Occurrence.
            dwca_occurrence_id = dwca_sample_id
            dwca_occurrence_id_short = dwca_sample_id_short
            scientific_name = row_dict.get('scientific_name', '')
            if scientific_name:
                key_list = [
                            ('scientific_name', 'scientific_name'), 
                           ]
                dwca_occurrence_id = dwca_sample_id
                extra_keys = self._create_extra_key(row_dict, key_list)
                if extra_keys:
                    dwca_occurrence_id += ':' + extra_keys
                row_dict['dwca_occurrence_id'] = dwca_occurrence_id
                row_dict['dwca_occurrence_id_md5'] = hashlib.md5(dwca_occurrence_id).hexdigest()
#                 # Used to generate short names.
#                 dwca_occurrence_id_short = dwca_sample_id_short + ':' + scientific_name
#                 row_dict['dwca_occurrence_id_short'] = dwca_occurrence_id_short
                # Used to generate short names.
                if dwca_occurrence_id not in self.dwca_occurrence_id_short_names:
                    self.dwca_occurrence_id_short_names.append(dwca_occurrence_id)
                dwca_occurrence_id_short = dwca_occurrence_id_short + ':' + 'TAXA-' + str(self.dwca_occurrence_id_short_names.index(dwca_occurrence_id) + 1)
                row_dict['dwca_occurrence_id_short'] = dwca_occurrence_id_short
     
            # MoF.
            key_list = [
                        ('param', 'parameter'), 
                        ('unit', 'unit'), 
                       ]
            dwca_mof_id = dwca_occurrence_id
            extra_keys = self._create_extra_key(row_dict, key_list)
            if extra_keys:
                dwca_mof_id += ':' + extra_keys
            row_dict['dwca_mof_id'] = dwca_mof_id
            row_dict['dwca_mof_id_md5'] = hashlib.md5(dwca_mof_id).hexdigest()
        except:
            print('DEBUG ', dwca_visit_id)
    
    def get_default_mapping(self):
        """ Implementation of abstract method declared in DwcaDatatypeBase. """
        if not self.dwca_default_mapping:
            self.dwca_default_mapping = {
                'eventID': 'shark_sample_id_md5', 
#                 'parentEventID': '', 
                'samplingProtocol': 'method_reference_code', 
##                'sampleSizeValue': 'sampled_volume_l',
#                 'sampleSizeUnit': '', # VALUE='l'
#                 'samplingEffort': '', 
                'eventDate': 'sample_date', 
                'eventTime': 'sample_time', 
#                 'startDayOfYear': '', 
#                 'endDayOfYear': '', 
                'year': 'visit_year', 
#                 'month': '', # AUTO.
#                 'day': '', # AUTO.
#                 'verbatimEventDate': '', 
#                 'habitat': '', 
#                 'fieldNumber': '', 
                'fieldNotes': 'visit_comment', 
                'eventRemarks': 'sample_comment', 
#                 'locationID': '', 
#                 'country': '', 
#                 'countryCode': '', 
##                'county': 'location_county', 
##                'municipality': 'location_municipality', 
#                 'locality': '', 
                'verbatimLocality': 'station_name', 
##                'waterBody': 'location_sea_basin',
#                 'verbatimDepth': '', 
##                'minimumDepthInMeters': 'sample_min_depth_m', 
##                'maximumDepthInMeters': 'sample_max_depth_m', 
                'decimalLatitude': 'sample_latitude_dd', 
                'decimalLongitude': 'sample_longitude_dd', 
#                 'geodeticDatum': '', 
#                 'type': '', 
#                 'modified': '', 
#                 'license': '', 
                'rightsHolder': 'sample_orderer_name_sv', # 'orderer_code', 
#                 'accessRights': '', 
#                 'bibliographicCitation': '', 
#                 'references': '', 
#                 'institutionID': '', 
#                 'datasetID': '', 
#                 'institutionCode': '', 
                'datasetName': 'dataset_file_name', 
                'ownerInstitutionCode': 'sample_orderer_name_sv', # 'orderer_code', 
#                 'dataGeneralizations': '', # (ex: aggregerad över storleksklass...)
#                 'dynamicProperties': '', 

                'recordedBy': 'sampling_laboratory_name_sv', # sampling_laboratory_code
                'scientificName': 'scientific_name', 
##                'measurementDeterminedDate': 'analysis_date', 
                'measurementDeterminedBy': 'analytical_laboratory_name_sv', # analysed_by
                'measurementRemarks': 'variable_comment', 
                'organismQuantity': 'value',
                'organismQuantityType': 'parameter',
                
##                'recordedBy': 'analysed_by',
            }
        #
        return self.dwca_default_mapping

