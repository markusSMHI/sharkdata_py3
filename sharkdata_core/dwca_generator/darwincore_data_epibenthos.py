#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-present SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import hashlib
from . import darwincore_data_base

class DarwinCoreDataEpibenthos(darwincore_data_base.DarwinCoreDataBase):
    """ """
    def __init__(self):
        """ """
        #
        super(DarwinCoreDataEpibenthos, self).__init__()
        # 
        self.dwca_default_mapping = []
        self.indata_visit_event_key_columns = []
        self.indata_sample_event_key_columns = []
        self.indata_occurrence_keys = []
        self.indata_measurementorfact_key_columns = []
        
        self.epibentos_visit_id_short_names = []
        self.epibentos_transect_id_short_names = []
        self.epibentos_section_id_short_names = []
        self.epibentos_occurrence_id_short_names = []
        
        self.occurrence_dynamic_properties_items = None
        self.event_transect_dynamic_properties_items = None
        
        self.sampling_event_key_list = None
        self.transect_key_list = None
        self.section_key_list = None
        self.occurrence_key_list = None
        self.emof_key_list = None
        
    def add_extra_fields(self, row_dict):
        """ Implementation of abstract method declared in DwcaDatatypeBase. """
        
        row_dict['collection_code'] = 'SHARK Epibenthos'
        row_dict['country'] = 'Sweden'
        row_dict['countryCode'] = 'SE'                
        row_dict['institutionCode'] = 'SMHI'
        #
#         if row_dict.get('sampled_volume_l', ''):
#             row_dict['sampleSizeUnit'] = 'l'
#         if row_dict.get('sampler_area_m2', ''):
#             row_dict['sampleSizeUnit'] = 'm2'

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
        #
        orderer = row_dict.get('sample_orderer_name_sv', '')
        if orderer:    
            row_dict['ownerInstitutionCode'] = orderer
            row_dict['rightsHolder'] = orderer
        else:
            orderer = row_dict.get('sample_orderer_name_en', '')
            if orderer:    
                row_dict['ownerInstitutionCode'] = orderer
                row_dict['rightsHolder'] = orderer
            else:
                orderer = row_dict.get('sample_orderer', '')
                if orderer:    
                    row_dict['ownerInstitutionCode'] = orderer
                    row_dict['rightsHolder'] = orderer
                else:
                    orderer = row_dict.get('orderer_code', '')
                    if orderer:    
                        row_dict['ownerInstitutionCode'] = orderer
                        row_dict['rightsHolder'] = orderer
        #
        recorded_by = row_dict.get('taxonomist', '')
        if recorded_by:    
            row_dict['recordedBy'] = recorded_by
            row_dict['measurementDeterminedBy'] = recorded_by
        else:
            recorded_by = row_dict.get('analysed_by', '')
            if recorded_by:    
                row_dict['recordedBy'] = recorded_by
                row_dict['measurementDeterminedBy'] = recorded_by
            else:
                recorded_by = row_dict.get('sampled_by', '')
                if recorded_by:    
                    row_dict['recordedBy'] = recorded_by
                    row_dict['measurementDeterminedBy'] = recorded_by
                else:
                    recorded_by = row_dict.get('diver_name', '')
                    if recorded_by:    
                        row_dict['recordedBy'] = recorded_by
                        row_dict['measurementDeterminedBy'] = recorded_by
        
        # Occurrence - Dynamic properties. 
        dynamic_properties_list = []
        if row_dict.get('scientific_name', '') != str(row_dict.get('reported_scientific_name', '')):
            dynamic_properties_list.append('"ReportedScientificName":"' + str(row_dict.get('reported_scientific_name', '')) + '"')
        
        if self.occurrence_dynamic_properties_items is None:
            self.occurrence_dynamic_properties_items = {
                        'SizeClass': 'size_class', 
#                         'SpeciesFlagCode': 'species_flag_code', 
                        'SizeClassRangeMin': 'size_class_range_min', 
                        'SizeClassRangeMax': 'size_class_range_max', 
                        'Epibiont': 'epibiont', 
                        'Detached': 'detached', 
                        'Recruits': 'recruits', 
#                         'ReproductiveOrgans': 'reproductive_organs', 
                        'Bitemark': 'bitemark', 
                        'DegreeBiofouling': 'degree_biofouling', 
                        'TaxonPhoto': 'taxon_photo', 
                         }
        #
        for key, value in self.occurrence_dynamic_properties_items.items():
            if row_dict.get(value, None):
                dynamic_properties_list.append('"' + key + '":"' + str(row_dict.get(value, '')) + '"')
        #            
        if len(dynamic_properties_list) > 0:
            row_dict['occurrence-dynamicProperties'] = '{' + ', '.join(dynamic_properties_list) + '}'                 

        # Event-transect - Dynamic properties. 
        dynamic_properties_list = []
        if self.event_transect_dynamic_properties_items is None:
            self.event_transect_dynamic_properties_items = {
                        'StationMarking': 'station_marking', 
                        'StationExposure': 'station_exposure', 
                         }
        #
        for key, value in self.event_transect_dynamic_properties_items.items():
            if row_dict.get(value, None):
                dynamic_properties_list.append('"' + key + '":"' + str(row_dict.get(value, '')) + '"')
        #            
        if len(dynamic_properties_list) > 0:
            row_dict['eventTransect-dynamicProperties'] = '{' + ', '.join(dynamic_properties_list) + '}'                 



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

        # Add extra epibentos key for sampling event.
        if self.sampling_event_key_list is None:
            self.sampling_event_key_list = [('station', 'station_name'), 
                        ('date', 'sample_date'), 
                       ]
        epibentos_visit_id = self._create_extra_key(row_dict, self.sampling_event_key_list)
        row_dict['epibentos_visit_id'] = epibentos_visit_id
        
        # Used to generate short names.
        if epibentos_visit_id not in self.epibentos_visit_id_short_names:
            self.epibentos_visit_id_short_names.append(epibentos_visit_id)
        epibentos_visit_id_short = 'EVENT-' + str(self.epibentos_visit_id_short_names.index(epibentos_visit_id) + 1)
        row_dict['epibentos_visit_id_short'] = epibentos_visit_id_short
        
        # Transect.
        if self.transect_key_list is None:
            self.transect_key_list = [
                        ('lat', 'sample_latitude_dd'), 
                        ('long', 'sample_longitude_dd'), 
                        ('tr_deg', 'transect_direction_deg'), 
                        ('tr_start_lat', 'transect_start_latitude_dd'), 
                        ('tr_start_long', 'transect_start_longitude_dd'), 
                        ('tr_end_lat', 'transect_end_latitude_dd'), 
                        ('tr_end_long', 'transect_end_latitude_dd'),
                       ]
        epibentos_transect_id = epibentos_visit_id
        extra_keys = self._create_extra_key(row_dict, self.transect_key_list)
        if extra_keys:
            epibentos_transect_id += ':' + extra_keys
        row_dict['epibentos_transect_id'] = epibentos_transect_id
        row_dict['epibentos_transect_id_md5'] = hashlib.md5(epibentos_transect_id).hexdigest()
        
        # Used to generate short names.
        if epibentos_transect_id not in self.epibentos_transect_id_short_names:
            self.epibentos_transect_id_short_names.append(epibentos_transect_id)
        epibentos_transect_id_short = epibentos_visit_id_short + ':' + 'TRANS-' + str(self.epibentos_transect_id_short_names.index(epibentos_transect_id) + 1)
        row_dict['epibentos_transect_id_short'] = epibentos_transect_id_short
        
        # Section.
        if self.section_key_list is None:
            self.section_key_list = [
                        ('sample_id', 'sample_id'),
#                         ('sample_part_id', 'sample_part_id'),
                        ('sample_depth_m', 'sample_depth_m'),
                        ('stratum_code', 'stratum_code'),
                        #('stratum_code', 'stratum_code'),
                        #('stratum_code', 'stratum_code'),
                        #('stratum_code', 'stratum_code'),
                        #('stratum_code', 'stratum_code'),
                        
                        ('shark_transect_id_md5', 'shark_transect_id_md5'),
                        ('shark_sample_id_md5', 'shark_sample_id_md5'),
                        
                        ('sect_start_lat', 'section_start_latitude_dd'), 
                        ('sect_start_long', 'section_start_longitude_dd'), 
                        ('sect_end_lat', 'section_end_latitude_dd'), 
                        ('sect_end_long', 'section_end_longitude_dd'), 
                        ('sect_start_m', 'section_distance_start_m'), 
                        ('sect_end_m', 'section_distance_end_m'), 
                        ('sect_start_depth_m', 'section_start_depth_m'), 
                        ('sect_end_depth_m', 'section_end_depth_m'), 
                        
                        ('sed_depos', 'sediment_deposition_code'), 
                        ('sect_debris_cover', 'section_debris_cover'), 
                        
                       ]
        
        
        
# datatype + locationId + visit_date + station_name + 
# transect_id + 
# section_distance_start_m + section_distance_end_m + 
# section_start_depth_m + section_end_depth_m        
        
        
        
        epibentos_section_id = epibentos_transect_id
        extra_keys = self._create_extra_key(row_dict, self.section_key_list)
        if extra_keys:
            epibentos_section_id += ':' + extra_keys
        row_dict['epibentos_section_id'] = epibentos_section_id
        row_dict['epibentos_section_id_md5'] = hashlib.md5(epibentos_section_id).hexdigest()
        
        # Used to generate short names.
        if epibentos_section_id not in self.epibentos_section_id_short_names:
            self.epibentos_section_id_short_names.append(epibentos_section_id)
        epibentos_section_id_short =  epibentos_transect_id_short + ':' + 'SECT-' + str(self.epibentos_section_id_short_names.index(epibentos_section_id) + 1)
        row_dict['epibentos_section_id_short'] = epibentos_section_id_short


        # Occurrence.
        epibentos_occurrence_id = epibentos_section_id
        epibentos_occurrence_id_short = epibentos_section_id_short
        scientific_name = row_dict.get('scientific_name', '')
        if scientific_name:
            if self.occurrence_key_list is None:
                self.occurrence_key_list = [
                            ('scientific_name', 'scientific_name'), 
                            ('detached', 'detached'), 
                            ('epibiont', 'epibiont'), 
    
                            ('species_flag_code', 'species_flag_code'), 
                            ('size_class', 'size_class'), 
                            ('degree_biofouling', 'degree_biofouling'), 
                            ('bitemark', 'bitemark'), 
                            ('reproductive_organs', 'reproductive_organs'), 
                            ('stratum_code', 'stratum_code'), 
    
                            ('reported_scientific_name', 'reported_scientific_name'), 
                            
                           ]
            epibentos_occurrence_id = epibentos_section_id
            extra_keys = self._create_extra_key(row_dict, self.occurrence_key_list)
            if extra_keys:
                epibentos_occurrence_id += ':' + extra_keys
            row_dict['epibentos_occurrence_id'] = epibentos_occurrence_id
#             row_dict['epibentos_occurrence_id_md5'] = hashlib.md5(epibentos_occurrence_id).hexdigest()
#             # Used to generate short names.
#             epibentos_occurrence_id_short = epibentos_section_id_short + ':' + scientific_name
#             row_dict['epibentos_occurrence_id_short'] = epibentos_occurrence_id_short
            # Used to generate short names.
            if epibentos_occurrence_id not in self.epibentos_occurrence_id_short_names:
                self.epibentos_occurrence_id_short_names.append(epibentos_occurrence_id)
            epibentos_occurrence_id_short = epibentos_section_id_short + ':' + 'TAXA-' + str(self.epibentos_occurrence_id_short_names.index(epibentos_occurrence_id) + 1)
            row_dict['epibentos_occurrence_id_short'] = epibentos_occurrence_id_short


        # MoF.
        if self.emof_key_list is None:
            self.emof_key_list = [
                        ('param', 'parameter'), 
                        ('unit', 'unit'), 
                        
                        
                        ('variable_comment', 'variable_comment'), 
                        
#                         ('sediment_deposition_code', 'sediment_deposition_code'), 
#                         ('section_debris_cover', 'section_debris_cover'), 
                        
                       ]
        epibentos_mof_id = epibentos_occurrence_id
        extra_keys = self._create_extra_key(row_dict, self.emof_key_list)
        if extra_keys:
            epibentos_mof_id += ':' + extra_keys
        row_dict['epibentos_mof_id'] = epibentos_mof_id
#         row_dict['epibentos_mof_id_md5'] = hashlib.md5(epibentos_mof_id).hexdigest()

    
    def get_default_mapping(self):
        """ Implementation of abstract method declared in DwcaDatatypeBase. """
        if not self.dwca_default_mapping:
            self.dwca_default_mapping = {
#                 'eventID': 'shark_sample_id_md5', 
#                 'parentEventID': '', 
                'samplingProtocol': 'method_documentation', #'method_reference_code', 
#                 'sampleSizeValue': 'sampled_volume_l',
#                 'sampleSizeUnit': '', # VALUE='l'
#                 'sampleSizeValue': 'sampler_area_m2',
                'sampleSizeUnit': '', # VALUE='m2'
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
                'eventRemarks': 'visit_comment', 
                'fieldNotes': 'sample_comment', 
#                 'locationID': '', 
#                 'country': '', 
#                 'countryCode': '', 
                'county': 'location_county', 
                'municipality': 'location_municipality', 
                'locality': 'station_cluster', 
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
#                 'rightsHolder': 'orderer_code', 
#                 'accessRights': '', 
#                 'bibliographicCitation': '', 
#                 'references': '', 
#                 'institutionID': '', 
#                 'datasetID': '', 
#                 'institutionCode': '', 
                'datasetName': 'dataset_file_name', 
#                 'ownerInstitutionCode': 'orderer_code', 
#                 'dataGeneralizations': '', # (ex: aggregerad �ver storleksklass...)
#                 'dynamicProperties': '', 

                'recordedBy': 'sampling_laboratory_code', 

#                 'scientificName': 'scientific_name', 
                'scientificName': 'reported_scientific_name', 

                'measurementRemarks': 'variable_comment', 
                'organismQuantity': 'value',
                'organismQuantityType': 'parameter',
                
                'reproductiveCondition': 'reproductive_organs', 
                'identificationQualifier': 'species_flag_code', 

                
                
#                 'recordedBy': 'analysed_by',
                
                
#                 'minimumDepthInMeters': 'sample_min_depth_m', 
####                'minimumDepthInMeters': 'section_start_depth_m', 
#                 'maximumDepthInMeters': 'sample_max_depth_m', 
####                'maximumDepthInMeters': 'section_end_depth_m', 
#                 'measurementDeterminedBy': 'analysed_by', 
                'measurementDeterminedBy':'taxonomist',
#                 'measurementMethod': 'analysis_method_code', 
                'measurementMethod':'method_documentation',
#                'measurementDeterminedDate': 'analysis_date', 
                'measurementDeterminedDate ':'sample_date',
                
            }
        #
        return self.dwca_default_mapping

### SHARK header for the datatype Epibenthos:
# 
# # delivery_datatype
# # check_status_sv
# # data_checked_by_sv
# # visit_year
# # station_name
# # reported_station_name
# # station_photo
# # station_cluster
# # station_exposure
# # station_marking
# # sample_project_name_sv
# # sample_orderer_name_sv
# # platform_code
# # visit_id
# # expedition_id
# # sample_date
# # sample_latitude_dm
# # sample_longitude_dm
# # sample_latitude_dd
# # sample_longitude_dd
# # positioning_system_code
# # wind_direction_code
# # wind_speed_ms
# # wave_exposure_fetch
# # wave_height_m
# # secchi_depth_m
# # secchi_depth_quality_flag
# # visit_comment
# # water_level_deviation_m
# # sample_cluster
# # sample_series
# # sample_id
# # sample_depth_m
# # sampling_laboratory_name_sv
# # sampler_type_code
# # sampler_area_cm2
# # sample_comment
# # scientific_name
# # species_flag_code
# # dyntaxa_id
# # parameter
# # value
# # unit
# # calc_by_dc
# # size_class
# # degree_biofouling
# # bitemark
# # reproductive_organs
# # detached
# # epibiont
# # stratum_code
# # taxon_photo
# # taxonomist
# # analysis_method_code
# # method_documentation
# # method_comment
# # image_id
# # fauna_flora_found
# # sediment_deposition_code
# # diver_name
# # sampler_area_m2
# # video_interpreted
# # sample_photo_code
# # variable_comment
# # analytical_laboratory_name_sv
# # analysed_by
# # preservation_method_code
# # bottom_slope_deg
# # transect_comment
# # transect_direction_deg
# # transect_start_latitude_dd
# # transect_start_longitude_dd
# # transect_end_latitude_dd
# # transect_end_longitude_dd
# # shark_transect_id_md5
# # transect_length_m
# # transect_max_depth_m
# # transect_min_depth_m
# # transect_max_distance_m
# # transect_min_distance_m
# # transect_video
# # transect_width_m
# # sample_substrate_cover_boulder
# # sample_substrate_comnt_boulder
# # sample_substrate_cover_rock
# # sample_substrate_comnt_rock
# # sample_substrate_cover_softbottom
# # sample_substrate_comnt_softbottom
# # sample_substrate_cover_stone
# # sample_substrate_comnt_stone
# # sample_substrate_cover_gravel
# # sample_substrate_comnt_gravel
# # sample_substrate_cover_sand
# # sample_substrate_comnt_sand
# # section_bare_substrate
# # section_comment
# # section_substrate_cover_boulder
# # section_substrate_comnt_boulder
# # section_substrate_cover_gravel
# # section_substrate_comnt_gravel
# # section_substrate_cover_rock
# # section_substrate_comnt_rock
# # section_substrate_cover_sand
# # section_substrate_comnt_sand
# # section_substrate_cover_softbottom
# # section_substrate_comnt_softbottom
# # section_substrate_cover_stone
# # section_substrate_comnt_stone
# # section_debris_cover
# # section_start_latitude_dd
# # section_start_longitude_dd
# # section_end_latitude_dd
# # section_end_longitude_dd
# # section_distance_start_m
# # section_distance_end_m
# # section_fauna_flora_found
# # section_start_depth_m
# # section_end_depth_m
# # location_water_category
# # location_water_district
# # location_svar_sea_area_name
# # location_svar_sea_area_code
# # location_type_area
# # location_sea_basin
# # location_helcom_ospar_area
# # location_economic_zone
# # location_county
# # location_municipality
# # station_viss_eu_id
# # water_land_station_type_code
# # monitoring_station_type_code
# # monitoring_purpose_code
# # monitoring_program_code
# # taxon_kingdom
# # taxon_phylum
# # taxon_class
# # taxon_order
# # taxon_family
# # taxon_genus
# # taxon_species
# # taxon_hierarchy
# # taxon_red_list_category
# # reported_scientific_name
# # reported_parameter
# # reported_value
# # reported_unit
# # reporting_institute_name_sv
# # data_holding_centre
# # internet_access
# # dataset_name
# # dataset_file_name
