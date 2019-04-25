#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import hashlib
from . import darwincore_data_base

class DarwinCoreDataZoobenthos(darwincore_data_base.DarwinCoreDataBase):
    """ """
    def __init__(self):
        """ """
        #
        super(DarwinCoreDataZoobenthos, self).__init__()
        # 
        self.dwca_default_mapping = []
        self.indata_visit_event_key_columns = []
        self.indata_sample_event_key_columns = []
        self.indata_occurrence_keys = []
        self.indata_measurementorfact_key_columns = []
        
        self.zoobenthos_visit_id_short_names = []
        self.zoobenthos_sample_id_short_names = []
        self.zoobenthos_occurrence_id_short_names = []
        
    def add_extra_fields(self, row_dict):
        """ Implementation of abstract method declared in DwcaDatatypeBase. """
        
        row_dict['collection_code'] = 'SHARK Zooplankton' 
        row_dict['country'] = 'Sweden' 
        row_dict['countryCode'] = 'SE'
        row_dict['institutionCode'] = 'SMHI'
        #
        if row_dict.get('sampled_volume_l', ''):
            row_dict['sampleSizeUnit'] = 'l'

        row_dict['basisOfRecord'] = 'HumanObservation'

        self.generated_parameters = {}
        #
        try:
            sample_date_str = str(row_dict['sample_date'])
#             row_dict['year'] = sample_date_str[0:4]
            row_dict['month'] = sample_date_str[5:7]
            row_dict['day'] = sample_date_str[8:10]
        except:
            pass
         
#         # Sampling effort.
#         self.sampling_effort_items = {'SampledVolume(l)': 'sampled_volume_l', 
#                                       'AnalysedVolume(cm3)': 'analysed_volume_cm3'}
#         if len(self.sampling_effort_items) > 0:
#             sampling_effort_list = []
#             for key, value in self.sampling_effort_items.items():
#                 if row_dict.get(value, None):
#                     sampling_effort_list.append('"' + key + '":"' + str(row_dict.get(value, '')) + '"')
#             if len(sampling_effort_list) > 0:
#                 row_dict['samplingEffort'] = '{' + ', '.join(sampling_effort_list) + '}' 
#    
#         # Sampling protocol. 
#         self.sampling_protocol_items = {'SamplerTypeCode': 'sampler_type_code', 
#                                         'MethodReference': 'method_reference_code'}        
#         if len(self.sampling_protocol_items) > 0:
#             sampling_protocol_list = []
#             for key, value in self.sampling_protocol_items.items():
#                 if row_dict.get(value, None):
#                     sampling_protocol_list.append('"' + key + '":"' + str(row_dict.get(value, '')) + '"')
#             if len(sampling_protocol_list) > 0:
#                 row_dict['samplingProtocol'] = '{' + ', '.join(sampling_protocol_list) + '}' 
# 
#         # Dynamic properties. Used for Size classes in Phytoplancton etc. 
#         self.dynamic_properties_items = {}
#         if len(self.dynamic_properties_items) > 0:
#             dynamic_properties_list = []
#             for key, value in self.dynamic_properties_items.items():
#                 if row_dict.get(value, None):
#                     dynamic_properties_list.append('"' + key + '":"' + str(row_dict.get(value, '')) + '"')
#             if len(dynamic_properties_list) > 0:
#                 row_dict['dynamicProperties'] = '{' + ', '.join(dynamic_properties_list) + '}'                 
#            
#             
#         # Identification Qualifier. Used for species related qualifiers. 
#         self.identification_qualifier_items = {}
#         if len(self.identification_qualifier_items) > 0:
#             identification_qualifier_list = []
#             for key, value in self.identification_qualifier_items.items():
#                 if row_dict.get(value, None):
#                     identification_qualifier_list.append('"' + key + '":"' + str(row_dict.get(value, '')) + '"')
#             if len(identification_qualifier_list) > 0:
#                 row_dict['identificationQualifier'] = '{' + ', '.join(identification_qualifier_list) + '}' 
#          
#          
#         # Field_number. Used for sample_id, sample_part_id, etc. 
#         self.field_number_items = ['sample_series', 
#                                    'sample_id', 
#                                    'sample_part_id'] 
#         if len(self.field_number_items) > 0:
#             field_number_list = []
#             for key in self.field_number_items:
#                 if row_dict.get(key, None):
#                     field_number_list.append(str(row_dict.get(key, '')))
#             row_dict['fieldNumber'] = '-'.join(field_number_list)  
                           
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

        # Add extra key for sampling event.
        key_list = [('station', 'station_name'), 
                    ('date', 'sample_date'), 
                   ]
        zoobenthos_visit_id = self._create_extra_key(row_dict, key_list)
        row_dict['zoobenthos_visit_id'] = zoobenthos_visit_id
        
        # Used to generate short names.
        if zoobenthos_visit_id not in self.zoobenthos_visit_id_short_names:
            self.zoobenthos_visit_id_short_names.append(zoobenthos_visit_id)
        zoobenthos_visit_id_short = 'EVENT-' + str(self.zoobenthos_visit_id_short_names.index(zoobenthos_visit_id) + 1)
        row_dict['zoobenthos_visit_id_short'] = zoobenthos_visit_id_short
        
        # Sample.
        key_list = [
                     ('shark_sample_id_md5', 'shark_sample_id_md5'),
                   ]
        zoobenthos_sample_id = zoobenthos_visit_id
        extra_keys = self._create_extra_key(row_dict, key_list)
        if extra_keys:
            zoobenthos_sample_id += ':' + extra_keys
        row_dict['zoobenthos_sample_id'] = zoobenthos_sample_id
        row_dict['zoobenthos_sample_id_md5'] = hashlib.md5(zoobenthos_sample_id).hexdigest()
        
        # Used to generate short names.
        if zoobenthos_sample_id not in self.zoobenthos_sample_id_short_names:
            self.zoobenthos_sample_id_short_names.append(zoobenthos_sample_id)
        zoobenthos_sample_id_short = zoobenthos_visit_id_short + ':' + 'SAMPLE-' + str(self.zoobenthos_sample_id_short_names.index(zoobenthos_sample_id) + 1)
        row_dict['zoobenthos_sample_id_short'] = zoobenthos_sample_id_short
        
        # Occurrence.
        zoobenthos_occurrence_id = zoobenthos_sample_id
        zoobenthos_occurrence_id_short = zoobenthos_sample_id_short
        scientific_name = row_dict.get('scientific_name', '')
        if scientific_name:
            key_list = [
                        ('sample_part_id', 'sample_part_id'), 
                        ('scientific_name', 'scientific_name'), 
                        ('dev_stage_code', 'dev_stage_code'), 
                       ]
            zoobenthos_occurrence_id = zoobenthos_sample_id
            extra_keys = self._create_extra_key(row_dict, key_list)
            if extra_keys:
                zoobenthos_occurrence_id += ':' + extra_keys
            row_dict['zoobenthos_occurrence_id'] = zoobenthos_occurrence_id
            # Used to generate short names.
            if zoobenthos_occurrence_id not in self.zoobenthos_occurrence_id_short_names:
                self.zoobenthos_occurrence_id_short_names.append(zoobenthos_occurrence_id)
            zoobenthos_occurrence_id_short = zoobenthos_sample_id_short + ':' + 'TAXA-' + str(self.zoobenthos_occurrence_id_short_names.index(zoobenthos_occurrence_id) + 1)
            row_dict['zoobenthos_occurrence_id_short'] = zoobenthos_occurrence_id_short

        # MoF.
        key_list = [
                    ('param', 'parameter'), 
                    ('unit', 'unit'), 
                   ]
        zoobenthos_mof_id = zoobenthos_occurrence_id
        extra_keys = self._create_extra_key(row_dict, key_list)
        if extra_keys:
            zoobenthos_mof_id += ':' + extra_keys
        row_dict['zoobenthos_mof_id'] = zoobenthos_mof_id
#         row_dict['zoobenthos_mof_id_md5'] = hashlib.md5(zoobenthos_mof_id).hexdigest()

    
    def get_default_mapping(self):
        """ Implementation of abstract method declared in DwcaDatatypeBase. """
        if not self.dwca_default_mapping:
            self.dwca_default_mapping = {
#                 'eventID': 'shark_sample_id_md5', 
#                 'parentEventID': '', 
                'samplingProtocol': 'method_reference_code', 
                'sampleSizeValue': 'sampled_volume_l',
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
                'county': 'location_county', 
                'municipality': 'location_municipality', 
#                 'locality': '', 
                'verbatimLocality': 'station_name', 
                'waterBody': 'location_sea_basin',
#                 'verbatimDepth': '', 
                'minimumDepthInMeters': 'sample_min_depth_m', 
                'maximumDepthInMeters': 'sample_max_depth_m', 
                'decimalLatitude': 'sample_latitude_dd', 
                'decimalLongitude': 'sample_longitude_dd', 
#                 'geodeticDatum': '', 
#                 'type': '', 
#                 'modified': '', 
#                 'license': '', 
                'rightsHolder': 'orderer_code', 
#                 'accessRights': '', 
#                 'bibliographicCitation': '', 
#                 'references': '', 
#                 'institutionID': '', 
#                 'datasetID': '', 
#                 'institutionCode': '', 
                'datasetName': 'dataset_file_name', 
                'ownerInstitutionCode': 'orderer_code', 
#                 'dataGeneralizations': '', # (ex: aggregerad �ver storleksklass...)
#                 'dynamicProperties': '', 
                'recordedBy': 'sampling_laboratory_code', 
                'scientificName': 'scientific_name', 
                'measurementRemarks': 'variable_comment', 
                'organismQuantity': 'value',
                'organismQuantityType': 'parameter',
                'recordedBy': 'analysed_by',
                'minimumDepthInMeters': 'sample_min_depth_m', 
                'maximumDepthInMeters': 'sample_max_depth_m', 
#                 'measurementDeterminedBy': 'analysed_by', 
                'measurementDeterminedBy':'taxonomist',
#                 'measurementMethod': 'analysis_method_code', 
                'measurementMethod':'method_documentation',
                'measurementDeterminedDate': 'analysis_date', 
                'measurementDeterminedDate ':'sample_date',
                
            }
        #
        return self.dwca_default_mapping

# ### SHARK header for the datatype Zoobenthos:
# delivery_datatype
# check_status_sv
# data_checked_by_sv
# visit_year
# station_name
# reported_station_name
# station_cluster
# sample_project_name_sv
# sample_orderer_name_sv
# platform_code
# visit_id
# shark_sample_id_md5
# sample_date
# sample_time
# sample_latitude_dm
# sample_longitude_dm
# sample_latitude_dd
# sample_longitude_dd
# positioning_system_code
# water_depth_m
# wind_direction_code
# wind_speed_ms
# air_temperature_degc
# air_pressure_hpa
# weather_observation_code
# cloud_observation_code
# wave_observation_code
# wave_height_m
# ice_observation_code
# secchi_depth_m
# secchi_depth_quality_flag
# visit_comment
# sediment_type
# sample_id
# sample_min_depth_m
# sample_max_depth_m
# sampling_laboratory_name_sv
# sampling_laboratory_accreditated
# sampler_type_code
# sampled_volume_l
# sampler_area_cm2
# sample_comment
# scientific_name
# species_flag_code
# dyntaxa_id
# parameter
# value
# unit
# quality_flag
# calc_by_dc
# dev_stage_code
# sample_part_id
# taxonomist
# method_documentation
# method_reference_code
# fauna_flora_found
# factors_influencing_code
# variable_comment
# analytical_laboratory_name_sv
# analytical_laboratory_accreditated
# analysed_by
# analysis_date
# preservation_method_code
# upper_mesh_size_um
# lower_mesh_size_um
# number_of_portions
# counted_portions
# sample_part_min_cm
# sample_part_max_cm
# location_water_category
# location_water_district
# location_svar_sea_area_name
# location_svar_sea_area_code
# location_type_area
# location_sea_basin
# location_helcom_ospar_area
# location_economic_zone
# location_county
# location_municipality
# station_viss_eu_id
# water_land_station_type_code
# monitoring_station_type_code
# monitoring_purpose_code
# monitoring_program_code
# taxon_kingdom
# taxon_phylum
# taxon_class
# taxon_order
# taxon_family
# taxon_genus
# taxon_species
# taxon_hierarchy
# taxon_red_list_category
# reported_scientific_name
# reported_parameter
# reported_value
# reported_unit
# reporting_institute_name_sv
# data_holding_centre
# internet_access
# dataset_name
# dataset_file_name


