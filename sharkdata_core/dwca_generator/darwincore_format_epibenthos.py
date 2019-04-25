#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import copy
from . import darwincore_format_standard
from . import darwincore_utils

class DarwinCoreFormatEpibenthos(darwincore_format_standard.DarwinCoreFormatStandard):
    """ """
    def __init__(self):
        """ Darwin Core Archive Format base class. """
        #
        super(DarwinCoreFormatEpibenthos, self).__init__()
        #
        self.dwca_event_columns = []
        self.dwca_occurrence_columns = []
        self.dwca_measurementorfact_columns = []
        self.mof_extra_visit_params = None
        self.mof_extra_transect_params = None
        self.mof_extra_section_params = None
        self.mof_extra_sample_params = None
        self.mof_extra_occurrence_params = None
        #
        self._taxa_lookup_dict = {}
    
    def create_dwca_event(self, dwca_datatype_object):
        """ """
        used_visit_event_key_list = []
        used_transect_event_key_list = []
        used_section_event_key_list = []
        #
        for target_row in self.target_rows:
            # Get keys.
            epibentos_visit_id = target_row.get('epibentos_visit_id', '')
            epibentos_transect_id = target_row.get('epibentos_transect_id', '')
            epibentos_section_id = target_row.get('epibentos_section_id', '')
            
            epibentos_visit_id_short = target_row.get('epibentos_visit_id_short', '')
            epibentos_transect_id_short = target_row.get('epibentos_transect_id_short', '')
            epibentos_section_id_short = target_row.get('epibentos_section_id_short', '')
#             epibentos_occurrence_id_short = target_row.get('epibentos_occurrence_id_short', '')
            
            # Visit event.
            if epibentos_visit_id and (epibentos_visit_id not in used_visit_event_key_list):
                used_visit_event_key_list.append(epibentos_visit_id)
                #
                event_dict = {}
                for column_name in ['eventDate', 'verbatimLocality', 'decimalLatitude', 'decimalLongitude']:
                    event_dict[column_name] = target_row.get(column_name, '')
                #
                event_dict['type'] = 'Sampling event'
                event_dict['id'] = epibentos_visit_id_short
                event_dict['eventID'] = epibentos_visit_id_short
                event_dict['eventRemarks'] = target_row.get('visit_comment', '')
                event_dict['fieldNotes'] = ''
                event_dict['parentEventID'] = ''
#                 # Add key to dynamicProperties.
#                 event_dict['dynamicProperties'] = epibentos_visit_id
                #
                self.dwca_event.append(event_dict) 
            
            # Transect event.
            if epibentos_transect_id and (epibentos_transect_id not in used_transect_event_key_list):
                used_transect_event_key_list.append(epibentos_transect_id)
                
                event_dict = {}
                for column_name in self.get_event_columns():
                    value = str(target_row.get(column_name, ''))
                    if value:
                        event_dict[column_name] = value
                #
                event_dict['type'] = 'Transect'
                event_dict['id'] = epibentos_transect_id_short
                event_dict['eventID'] = epibentos_transect_id_short
                event_dict['parentEventID'] = epibentos_visit_id_short
                event_dict['eventRemarks'] = target_row.get('transect_comment', '')
                event_dict['fieldNotes'] = ''
                # Add key to dynamicProperties.
                event_dict['dynamicProperties'] = target_row.get('eventTransect-dynamicProperties', '')
                # Clear some values.
                event_dict['minimumDepthInMeters'] = ''
                event_dict['maximumDepthInMeters'] = ''
                
                
                event_dict['sampleSizeValue'] = ''
                event_dict['sampleSizeUnit'] = ''
                transect_length_m = target_row.get('transect_length_m', '')
                transect_width_m = target_row.get('transect_width_m', '')
                try:
                    if transect_length_m and transect_width_m:
                        area = float(transect_length_m) * float(transect_width_m)
                        event_dict['sampleSizeValue'] = area
                        event_dict['sampleSizeUnit'] = 'm2'
                except:
                    pass
                    #
                self.dwca_event.append(event_dict) 
            
            # Section event (similar to sample).
            if epibentos_section_id and (epibentos_section_id not in used_section_event_key_list):
                used_section_event_key_list.append(epibentos_section_id)
                
                event_dict = {}
                for column_name in self.get_event_columns():
                    value = str(target_row.get(column_name, ''))
                    if value:
                        event_dict[column_name] = value
                #
                event_dict['type'] = 'Section'
                event_dict['id'] = epibentos_section_id_short
                event_dict['eventID'] = epibentos_section_id_short
                event_dict['eventRemarks'] = ''
                #
                sample_cmnt = str(target_row.get('sample_comment', ''))
                sect_cmnt = str(target_row.get('section_comment', ''))
                if sample_cmnt and sect_cmnt:
                    event_dict['fieldNotes'] = sample_cmnt + '   ' + sect_cmnt
                else:
                    event_dict['fieldNotes'] = sample_cmnt + sect_cmnt
                #
                event_dict['parentEventID'] = epibentos_transect_id_short
#                 # Add key to dynamicProperties.
#                 event_dict['dynamicProperties'] = epibentos_section_id
                
#                 event_dict['occurrenceID'] = epibentos_occurrence_id_short
                
                self.dwca_event.append(event_dict) 
        
    def create_dwca_occurrence(self, dwca_datatype_object):
        """ """
        used_occurrence_key_list = []
        #
        for target_row in self.target_rows:
            scientific_name = target_row.get('scientific_name', '')
            if scientific_name == '':
                continue
            #
            epibentos_occurrence_id = target_row.get('epibentos_occurrence_id', '')
            epibentos_section_id_short = target_row.get('epibentos_section_id_short', '')
            epibentos_occurrence_id_short = target_row.get('epibentos_occurrence_id_short', '')
            #
            if epibentos_occurrence_id and (epibentos_occurrence_id not in used_occurrence_key_list):
                used_occurrence_key_list.append(epibentos_occurrence_id)
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
                occurrence_dict['id'] = epibentos_section_id_short
                occurrence_dict['eventID'] = epibentos_section_id_short
                occurrence_dict['occurrenceID'] = epibentos_occurrence_id_short            
#                 # Add key to dynamicProperties.
#                 occurrence_dict['dynamicProperties'] = epibentos_occurrence_id
                occurrence_dict['dynamicProperties'] = target_row.get('occurrence-dynamicProperties', '')
                #
                self.dwca_occurrence.append(occurrence_dict) 
    
    def create_dwca_measurementorfact(self, dwca_datatype_object):
        """ Overridden method from base calss. """
        used_extra_params_visit_list = []
        used_extra_params_transect_list = []
        used_extra_params_section_list = []
        used_extra_params_occurrence_list = []
        used_mof_key_list = []
        
        debug_row_number = 0
        
        for target_row in self.target_rows:
            # Keys, both for values from enet and from occurrence.
            epibentos_visit_id = target_row.get('epibentos_visit_id', '')
            epibentos_transect_id = target_row.get('epibentos_transect_id', '')
            epibentos_section_id = target_row.get('epibentos_section_id', '')
            epibentos_occurrence_id = target_row.get('epibentos_occurrence_id', '')
            epibentos_mof_id = target_row.get('epibentos_mof_id', '')
            
            epibentos_visit_id_short = target_row.get('epibentos_visit_id_short', '')
            epibentos_transect_id_short = target_row.get('epibentos_transect_id_short', '')
            epibentos_section_id_short = target_row.get('epibentos_section_id_short', '')
            epibentos_occurrence_id_short = target_row.get('epibentos_occurrence_id_short', '')
            
            # Connect to event, transect or section. Compare keys and use short keys.
            event_key = epibentos_section_id_short
            if epibentos_visit_id == epibentos_section_id:
                event_key = epibentos_visit_id_short
            elif epibentos_transect_id == epibentos_section_id:
                event_key = epibentos_transect_id_short
                
            # Extra parameters from column values. Visit level.
            if epibentos_visit_id and (epibentos_visit_id not in used_extra_params_visit_list):
                used_extra_params_visit_list.append(epibentos_visit_id)
                if self.mof_extra_visit_params is None:
                    self.mof_extra_visit_params = {
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
                    }
                for key, (param, unit) in self.mof_extra_visit_params.iteritems(): 
                    value = str(target_row.get(key, ''))
                    if value: 
                        measurementorfact_dict = {} 
                        measurementorfact_dict['id'] = epibentos_visit_id_short 
                        measurementorfact_dict['eventID'] = epibentos_visit_id_short 
                        measurementorfact_dict['measurementType'] = param 
                        measurementorfact_dict['measurementValue'] = value 
                        measurementorfact_dict['measurementUnit'] = unit 
                        measurementorfact_dict['measurementDeterminedDate'] = target_row.get('sample_date', '') 
                        #
                        self.dwca_measurementorfact.append(measurementorfact_dict) 
            
            
            
            # Extra parameters from column values. Transect level.
            if epibentos_transect_id and (epibentos_transect_id not in used_extra_params_transect_list):
                used_extra_params_transect_list.append(epibentos_transect_id)
                if self.mof_extra_transect_params is None:
                    self.mof_extra_transect_params = {
                        'transect_length_m': ('Transect length', 'm'), 
                        'transect_width_m': ('Transect width', 'm'), 
                    }
                for key, (param, unit) in self.mof_extra_transect_params.iteritems(): 
                    value = str(target_row.get(key, ''))
                    if value: 
                        measurementorfact_dict = {} 
                        measurementorfact_dict['id'] = epibentos_transect_id_short 
                        measurementorfact_dict['eventID'] = epibentos_transect_id_short 
                        measurementorfact_dict['measurementType'] = param 
                        measurementorfact_dict['measurementValue'] = value 
                        measurementorfact_dict['measurementUnit'] = unit 
                        measurementorfact_dict['measurementDeterminedDate'] = target_row.get('sample_date', '') 
                        #
                        self.dwca_measurementorfact.append(measurementorfact_dict) 
            
            
            
            # Extra parameters from column values. Section level.
            if epibentos_section_id and (epibentos_section_id not in used_extra_params_section_list):
                used_extra_params_section_list.append(epibentos_section_id)
                if self.mof_extra_section_params is None:
                    self.mof_extra_section_params = {
                        'sampler_area_m2': ('Sampler area', 'm2'), 
                        'sampler_area_cm2': ('Sampler area', 'cm2'), 

                        'sediment_deposition_code': ('Sediment deposition code', ''),
                        'section_debris_cover': ('Section debris cover', '%'), 
                        
                    }
                for key, (param, unit) in self.mof_extra_section_params.iteritems(): 
                    value = str(target_row.get(key, ''))
                    if value: 
                        measurementorfact_dict = {} 
                        measurementorfact_dict['id'] = epibentos_section_id_short 
                        measurementorfact_dict['eventID'] = epibentos_section_id_short 
                        measurementorfact_dict['measurementType'] = param 
                        measurementorfact_dict['measurementValue'] = value 
                        measurementorfact_dict['measurementUnit'] = unit 
                        measurementorfact_dict['measurementDeterminedDate'] = target_row.get('sample_date', '') 
                        #
                        self.dwca_measurementorfact.append(measurementorfact_dict) 
            
            # Used if row contains species.
            occurrence_key = epibentos_occurrence_id_short
            if epibentos_occurrence_id == epibentos_section_id:
                occurrence_key = ''
            else:
            
            
                if epibentos_occurrence_id and (epibentos_occurrence_id not in used_extra_params_occurrence_list):
                    used_extra_params_occurrence_list.append(epibentos_occurrence_id)
                    if self.mof_extra_occurrence_params is None:
                        self.mof_extra_occurrence_params = {
                            'size_class': ('Size class', ''), 
#                             'species_flag_code': ('Species flag code', ''), 
                            'size_class_range_min': ('Size class range min', ''), 
                            'size_class_range_max': ('Size class range max', ''), 
                            'epibiont': ('Epibiont', ''), 
                            'detached': ('Detached', ''), 
                            'recruits': ('Recruits', ''), 
#                             'reproductive_organs': ('Reproductive organs', ''), 
                            'bitemark': ('Bitemark', ''), 
                            'degree_biofouling': ('Degree biofouling', ''), 
                        }
                    for key, (param, unit) in self.mof_extra_occurrence_params.iteritems(): 
                        value = str(target_row.get(key, ''))
                        if value: 
                            measurementorfact_dict = {} 
                            measurementorfact_dict['id'] = epibentos_section_id_short 
                            measurementorfact_dict['eventID'] = epibentos_section_id_short 
                            measurementorfact_dict['occurrenceID'] = occurrence_key
                            measurementorfact_dict['measurementType'] = param 
                            measurementorfact_dict['measurementValue'] = value 
                            measurementorfact_dict['measurementUnit'] = unit 
                            measurementorfact_dict['measurementDeterminedDate'] = target_row.get('sample_date', '') 
                            measurementorfact_dict['measurementDeterminedDate'] = target_row.get('analysis_date', '')
                            measurementorfact_dict['measurementDeterminedBy'] = target_row.get('analysed_by', '')
                            measurementorfact_dict['measurementMethod'] = target_row.get('analysis_method_code', '') # TODO: method_reference_code
                            measurementorfact_dict['measurementRemarks'] = target_row.get('variable_comment', '')
                            #
                            self.dwca_measurementorfact.append(measurementorfact_dict) 
            
            # eMoF rows.
            if epibentos_mof_id and (epibentos_mof_id not in used_mof_key_list):
                used_mof_key_list.append(epibentos_mof_id)
            
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
                    measurementorfact_dict['measurementDeterminedDate'] = target_row.get('sample_date', '') 
                    measurementorfact_dict['measurementDeterminedDate'] = target_row.get('analysis_date', '')
                    measurementorfact_dict['measurementDeterminedBy'] = target_row.get('analysed_by', '')
                    measurementorfact_dict['measurementMethod'] = target_row.get('analysis_method_code', '') # TODO: method_reference_code
                    measurementorfact_dict['measurementRemarks'] = target_row.get('variable_comment', '')
                    #
                    self.dwca_measurementorfact.append(measurementorfact_dict)
            else:
                if debug_row_number < 100:
                    try:
                        print('DEBUG: epibentos_mof_id: ' + str(epibentos_mof_id))
                    except Exception as e:
                        print('DEBUG Exception: ' + str(e))
                    debug_row_number += 1
                elif debug_row_number == 100:
                    print('DEBUG: MAX LIMIT OF 100 LOG ROWS.')
                    debug_row_number += 1
    
    def get_event_columns(self):
        """ Implementation of abstract method declared in DwcaDatatypeBase. """
        if not self.dwca_event_columns:
            self.dwca_event_columns = [
                'id', 
                'eventID', 
                'parentEventID', 
                'type', 
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
                'eventRemarks', 
                'fieldNotes', 
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
                'samplingProtocol', 
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
                'dataGeneralizations', # (ex: aggregerad Ã¶ver storleksklass...)
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
                'reproductiveCondition', 
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
#                 'occurrenceRemarks',
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

