#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-present SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import numpy as np
import pandas as pd
import zipfile

from . import darwincore_utils
from . import darwincore_format_standard
from . import darwincore_format_epibenthos
from . import darwincore_data_epibenthos
from . import darwincore_data_zoobenthos
from . import darwincore_data_bacterioplankton
from . import darwincore_meta_xml
from . import darwincore_eml_xml
from . import darwincore_data_greyseal
from . import darwincore_data_harbourseal
from . import darwincore_data_ringedseal
from . import darwincore_data_phytoplankton_jerico

from . import darwincore_zip

class DarwinCoreWriter(object):
    """ Creates DarwinCore-Archive files for sample based data. """
    
    def __init__(self): 
        """ """
    
    def create_darwincore_archive(self, 
                                  datatype='Epibenthos', 
                                  # dataset_dir='D:/arnold/4_sharkdata/notebooks/test_data/epi_nationella', 
                                  dataset_dir='D:/arnold/4_sharkdata/notebooks/test_data/epi_nationella_ALLA', 
                                  national_data=True,
                                  out_file_path='D:/arnold/4_sharkdata/notebooks/test_data/dwca-epibenthos-obis.zip', 
                                  ): 
        """ Datatype: bacterioplankton, epibenthos, phytoplankton, zoobenthos, zooplankton. """
        #
        self.clear()
        #
        self.setup(datatype, national_data)
        #
        self.load_taxa()
        #
        self.load_export_filter()
        #
        dwca_zip = darwincore_zip.DarwinCoreZip(dwca_file_path=out_file_path)
        #
        dwca_zip.create_tmp_dir()
        #
        dwca_zip.write_event_header(self.dwca_format_object.get_event_columns())
        dwca_zip.write_occurrence_header(self.dwca_format_object.get_occurrence_columns())
        dwca_zip.write_measurementorfact_header(self.dwca_format_object.get_measurementorfact_columns())
        #
        errors_in_datasets = []
        #
#         for in_file_path in pathlib.Path(dataset_dir).glob('SHARK_Epibenthos_*.zip'):

        if datatype == 'Phytoplankton-JERICO-IFCB':
            file_template = 'SHARK_Phytoplankton_*JERICO*IFCB_version*.zip'
            self.datatype = 'phytoplankton'
        elif datatype == 'Phytoplankton-JERICO':
            file_template = 'SHARK_Phytoplankton_*JERICO_version*.zip'
            self.datatype = 'phytoplankton'
        else:
            file_template = 'SHARK_' + datatype + '_*.zip'
        for in_file_path in pathlib.Path(dataset_dir).glob(file_template):

            try:
                # Filter on national or regional data.
                dataset_name = pathlib.Path(in_file_path).name
                dataset_name = dataset_name.split('_version_')[0]
                
                if datatype not in ['GreySeal', 'HarbourSeal', 'RingedSeal', 
                                    'Phytoplankton-JERICO', 'Phytoplankton-JERICO-IFCB']:
                
                    if national_data:
                        # National data.
                        if dataset_name not in darwincore_utils.ExportFilter().get_filter_keep_list('dataset_name'):
                            print('DEBUG: NatNot included in filter: ' + dataset_name)
                            continue # Don't use this dataset.
                    else:
                        # Regional data.
                        if dataset_name in darwincore_utils.ExportFilter().get_filter_keep_list('dataset_name'):
                            print('DEBUG: Not included in filter: ' + dataset_name)
                            continue # Don't use this dataset.
                
                #
                self.generate_dwca_for_dataset(str(in_file_path))
                event_rows, occurrence_rows, emof_rows = self.dwca_format_object.get_rows()
                #
                dwca_zip.write_event_rows(event_rows)
                dwca_zip.write_occurrence_rows(occurrence_rows)
                dwca_zip.write_measurementorfact_rows(emof_rows)
            except Exception as e:
                print('EXCEPTION: ' + dataset_name + '  ' + str(e))
                errors_in_datasets.append((dataset_name, e))
                raise
        #
        # Recalculate the automatically generated part of metadata.
        self._calculate_auto_metadata()
        
        # EML
        dwca_eml_xml_rows = darwincore_eml_xml.DarwinCoreEmlXml().create_eml_xml(
                                                self.eml_template)
        if len(dwca_eml_xml_rows) > 1:
            for index, xml_row in enumerate(dwca_eml_xml_rows):
                if 'REPLACE-' in xml_row:                    
                    dwca_eml_xml_rows[index] = dwca_eml_xml_rows[index].replace('REPLACE-packageId', 'TODO-PACKAGE-ID')
                    dwca_eml_xml_rows[index] = dwca_eml_xml_rows[index].replace('REPLACE-pubDate', str(datetime.datetime.today().date()))
                    dwca_eml_xml_rows[index] = dwca_eml_xml_rows[index].replace('REPLACE-westBoundingCoordinate',  str(self._metadata_dict.get('longitude_dd_min', '')))
                    dwca_eml_xml_rows[index] = dwca_eml_xml_rows[index].replace('REPLACE-eastBoundingCoordinate',  str(self._metadata_dict.get('longitude_dd_max', '')))
                    dwca_eml_xml_rows[index] = dwca_eml_xml_rows[index].replace('REPLACE-northBoundingCoordinate',  str(self._metadata_dict.get('latitude_dd_max', '')))
                    dwca_eml_xml_rows[index] = dwca_eml_xml_rows[index].replace('REPLACE-southBoundingCoordinate',  str(self._metadata_dict.get('latitude_dd_min', '')))
                    dwca_eml_xml_rows[index] = dwca_eml_xml_rows[index].replace('REPLACE-beginDate-calendarDate',  str(self._metadata_dict.get('sample_date_min', '')))
                    dwca_eml_xml_rows[index] = dwca_eml_xml_rows[index].replace('REPLACE-endDate-calendarDate',  str(self._metadata_dict.get('sample_date_max', '')))
                    dwca_eml_xml_rows[index] = dwca_eml_xml_rows[index].replace('REPLACE-Parameters',  str(self._metadata_dict.get('parameter_list', '')))
            #
            dwca_zip.write_dwca_eml(dwca_eml_xml_rows)
        
        # META
        dwca_meta_xml_rows = darwincore_meta_xml.DarwinCoreMetaXml().create_meta_xml(
                                                self.dwca_format_object.get_event_columns(), 
                                                self.dwca_format_object.get_occurrence_columns(), 
                                                self.dwca_format_object.get_measurementorfact_columns(),
                                                )
        dwca_zip.write_dwca_meta(dwca_meta_xml_rows)
        #
        dwca_zip.create_darwingcore_zip_file(out_file_path)
        #
        self.log_missing_taxa()
        #
#######################################        dwca_zip.remove_tmp_dir()
        #
        if len(errors_in_datasets) > 0:
            print('')
            print('DEBUG: Errors in: ')
            for (dataset_name, e) in errors_in_datasets:
                print('- ' + dataset_name)
                print('  - ' + str(e))
            print('')
        
        
    def clear(self):
        """ """
        self.dwca_format_object = None
        self.dwca_datatype_object = None
        self.eml_template = None
        
#         self._data_df = None
        self._metadata_dict = {}
#         self._species_translate = {}
#         self._value_translate = {}
#         self._log_row_list = []
        # Metadata.
        self._metadata_year_min = []
        self._metadata_year_max = []
        self._metadata_sample_date_min = []
        self._metadata_sample_date_max = []
        self._metadata_latitude_dd_min = []
        self._metadata_latitude_dd_max = []
        self._metadata_longitude_dd_min = []
        self._metadata_longitude_dd_max = []
        self._metadata_parameter_list = []
        self._metadata_unit_list = []
    
    def setup(self, datatype, national_data): # Alternatives: bacterioplankton, epibenthos, phytoplankton, zoobenthos, zooplankton.
        """ """
        self.clear()
        #
        self.datatype = datatype.lower()        
        # Create format and datatype objects.
        if self.datatype in ['bacterioplankton']:
            self.dwca_format_object = darwincore_format_standard.DarwinCoreFormatStandard()
            self.dwca_datatype_object = darwincore_data_bacterioplankton.DarwinCoreDataBacterioplankton()
            self.eml_template = 'proj_sharkdata/proj_sharkdata/sharkdata_core/dwca_generator/templates/bacterioplankton_nat_eml.xml'
            
        elif self.datatype in ['epibenthos', 'phytobenthos', 'pb']:
            self.dwca_format_object = darwincore_format_epibenthos.DarwinCoreFormatEpibenthos()
            self.dwca_datatype_object = darwincore_data_epibenthos.DarwinCoreDataEpibenthos()
            if national_data:
    #             self.eml_template = 'proj_sharkdata/proj_sharkdata/sharkdata_core/dwca_generator/templates/epibenthos_nat_eml.xml'
                self.eml_template = 'templates/epibenthos_nat_eml.xml'
            else:
    #             self.eml_template = 'proj_sharkdata/proj_sharkdata/sharkdata_core/dwca_generator/templates/epibenthos_nat_eml.xml'
                self.eml_template = 'templates/epibenthos_reg_eml.xml'
            
        elif self.datatype in ['phytoplankton', 'pp']:
            print('TODO: phytoplankton.')
            
        elif self.datatype in ['zoobenthos', 'zb']:
            self.dwca_format_object = darwincore_format_standard.DarwinCoreFormatStandard()
            self.dwca_datatype_object = darwincore_data_zoobenthos.DarwinCoreDataZoobenthos()
            self.eml_template = 'proj_sharkdata/proj_sharkdata/sharkdata_core/dwca_generator/templates/zoobenthos_nat_eml.xml'
            
        elif self.datatype in ['zooplankton', 'zp']:
            print('TODO: zooplankton.')
            
        elif self.datatype in ['greyseal']:
            self.dwca_format_object = darwincore_format_standard.DarwinCoreFormatStandard()
            self.dwca_datatype_object = darwincore_data_greyseal.DarwinCoreDataGreySeal()
#             self.eml_template = 'proj_sharkdata/proj_sharkdata/sharkdata_core/dwca_generator/templates/greyseal_eml.xml'
            self.eml_template = 'templates/greyseal_eml.xml'
            
        elif self.datatype in ['harbourseal']:
            self.dwca_format_object = darwincore_format_standard.DarwinCoreFormatStandard()
            self.dwca_datatype_object = darwincore_data_harbourseal.DarwinCoreDataHarbourSeal()
#             self.eml_template = 'proj_sharkdata/proj_sharkdata/sharkdata_core/dwca_generator/templates/harbourseal_eml.xml'
            self.eml_template = 'templates/harbourseal_eml.xml'
        
        elif self.datatype in ['ringedseal']:
            self.dwca_format_object = darwincore_format_standard.DarwinCoreFormatStandard()
            self.dwca_datatype_object = darwincore_data_ringedseal.DarwinCoreDataRingedSeal()
#             self.eml_template = 'proj_sharkdata/proj_sharkdata/sharkdata_core/dwca_generator/templates/ringedseal_eml.xml'
            self.eml_template = 'templates/ringedseal_eml.xml'
        
        
        
        elif self.datatype in ['phytoplankton-jerico']:
            self.dwca_format_object = darwincore_format_standard.DarwinCoreFormatStandard()
            self.dwca_datatype_object = darwincore_data_phytoplankton_jerico.DarwinCoreDataPhytoplanktonJerico()
#             self.eml_template = 'proj_sharkdata/proj_sharkdata/sharkdata_core/dwca_generator/templates/ringedseal_eml.xml'
            self.eml_template = 'templates/phytoplankton_jerico_eml.xml'
        elif self.datatype in ['phytoplankton-jerico-ifcb']:
            self.dwca_format_object = darwincore_format_standard.DarwinCoreFormatStandard()
            self.dwca_datatype_object = darwincore_data_phytoplankton_jerico.DarwinCoreDataPhytoplanktonJerico()
#             self.eml_template = 'proj_sharkdata/proj_sharkdata/sharkdata_core/dwca_generator/templates/ringedseal_eml.xml'
            self.eml_template = 'templates/phytoplankton_jerico_ifcb_eml.xml'
        
        
        
        
        else:
            print('ERROR: Datatype not found.')
            return

    def load_taxa(self):
        """ """
        # Load resource content to translate from DynTaxa to WoRMS.
        darwincore_utils.TranslateTaxa().load_translate_taxa('translate_dyntaxa_to_valid_worms')
        
    def load_export_filter(self):
        """ """
        # Load resource content to translate from DynTaxa to WoRMS.
        darwincore_utils.ExportFilter().load_export_filter('TODO')
    
    def generate_dwca_for_dataset(self, data_table_path):
        """ """
        dataset_name = pathlib.Path(data_table_path).name
        dataset_name = dataset_name.split('_version_')[0]
        print('- Dataset: ' + str(dataset_name))
        
        suffix = pathlib.Path(data_table_path).suffix
        # If it is a single text file.
        if suffix == '.txt':
            data_df = pd.read_csv(data_table_path, 
                                  delimiter='\t', encoding='cp1252')
        # If it is a SHARK archive zip file.
        elif suffix == '.zip':
            
            if not 'shark_' + self.datatype in data_table_path.lower():
                print('ERROR: Wrong datatype :' + data_table_path)
                return 
            
            # From file in zip to dataframe.
            with zipfile.ZipFile(data_table_path) as z:
                with z.open('shark_data.txt') as f:
                    data_df = pd.read_csv(f, delimiter='\t', encoding='cp1252')
        # Replace nan values by ''.
        data_df.fillna('', inplace=True)
        
        # Create DwC-A content.
        self.dwca_format_object.clear()
        self.dwca_format_object.prepare_rows(data_df, self.dwca_datatype_object)

        # Create file content for DwC-A.
        self.dwca_format_object.create_dwca_parts(self.dwca_datatype_object)
        
        # Metadata
        self._metadata_year_min.append(int(data_df['visit_year'].min()))
        self._metadata_year_max.append(int(data_df['visit_year'].max()))
        self._metadata_sample_date_min.append(data_df['sample_date'].min())
        self._metadata_sample_date_max.append(data_df['sample_date'].max())

        sample_lat_min = float(data_df['sample_latitude_dd'].min())
        sample_lat_max = float(data_df['sample_latitude_dd'].max())
        sample_long_min = float(data_df['sample_longitude_dd'].min())
        sample_long_max = float(data_df['sample_longitude_dd'].max())
#         if (sample_lat_min > 0.0) and (sample_lat_max > 0.0) and \
#            (sample_long_min > 0.0) and (sample_long_max > 0.0):
        self._metadata_latitude_dd_min.append(sample_lat_min)
        self._metadata_latitude_dd_max.append(sample_lat_max)
        self._metadata_longitude_dd_min.append(sample_long_min)
        self._metadata_longitude_dd_max.append( sample_long_max)

        param_units = data_df.groupby(['parameter', 'unit']).size().reset_index().rename(columns={0:'count'})
        param_list = []
        unit_list = []
        for index, row in param_units.iterrows():
            param_list.append(row['parameter'])
            unit_list.append(row['unit'])
#             self._metadata_dict['parameter-' + str(index + 1)] = row['parameter']
#             self._metadata_dict['unit-' + str(index + 1)] = row['unit']
        #
        self._metadata_parameter_list += param_list
        self._metadata_unit_list += unit_list
    
    def _calculate_auto_metadata(self):
        """ Perform calculation of the automatically generated metadata if datasets are concatenated. """
        # Year.
        self._metadata_dict['year_min'] = int(np.nanmin(self._metadata_year_min))
        self._metadata_dict['year_max'] = int(np.nanmin(self._metadata_year_max))
        # Date.
        metadata_df = pd.DataFrame({
            'sample_date_min': self._metadata_sample_date_min, 
            'sample_date_max': self._metadata_sample_date_max, 
            })
        self._metadata_dict['sample_date_min'] = metadata_df['sample_date_min'].dropna().min()
        self._metadata_dict['sample_date_max'] = metadata_df['sample_date_max'].dropna().max()
        # Lat/long.
        self._metadata_dict['latitude_dd_min'] = format(np.nanmin(self._metadata_latitude_dd_min), '.4f')
        self._metadata_dict['latitude_dd_max'] = format(np.nanmax(self._metadata_latitude_dd_max), '.4f')
        self._metadata_dict['longitude_dd_min'] = format(np.nanmin(self._metadata_longitude_dd_min), '.4f')
        self._metadata_dict['longitude_dd_max'] = format(np.nanmax(self._metadata_longitude_dd_max), '.4f')
        # Params.
        metadata_params_df = pd.DataFrame({
            'parameter': self._metadata_parameter_list,
            'unit': self._metadata_unit_list,
            })
        param_units = metadata_params_df.groupby(['parameter', 'unit']).size().reset_index().rename(columns={0:'count'})
        param_list = []
        for index, row in param_units.iterrows():
            param_list.append(row['parameter'])
            self._metadata_dict['parameter-' + str(index + 1)] = row['parameter']
            self._metadata_dict['unit-' + str(index + 1)] = row['unit']
        #
        self._metadata_dict['parameter_list'] = ', '.join(param_list)
    
    def log_missing_taxa(self, dwca_file_path='darwincore_archive.zip'):
        """ """
        # Log missing taxa.
        missing_taxa_list = darwincore_utils.TranslateTaxa().get_missing_taxa_list()
        if len(missing_taxa_list) > 0:
#             admin_models.addResultLog(logrow_id, result_log = 'Missing taxa: ')
#             for missing_taxa in sorted(missing_taxa_list):
#                 admin_models.addResultLog(logrow_id, result_log = '- ' + missing_taxa)
#                 if settings.DEBUG: print('DEBUG: missing taxon: ' + missing_taxa)
#             admin_models.addResultLog(logrow_id, result_log = '')
            print('Missing taxa: ')
            for missing_taxa in sorted(missing_taxa_list):
                print('- ' + missing_taxa)
            print('')
    
    def save_dwca_file(self, dwca_file_path='darwincore_archive.zip'):
        """ """
        # Recalculate the automatically generated part of metadata.
        self._calculate_auto_metadata()
        # Write to file.
        self.dwca_format_object.save_to_archive_file(dwca_file_path, self.eml_template, self._metadata_dict)
    
    
    
##### TEST ######################################################################
if __name__ == "__main__":
    """ """
    import datetime
    print('TEST: Started. ' + str(datetime.datetime.now()))
    print('')

#     # JERICO.
#     print('')
#     print('')
#     print('TEST: JERICO. ' + str(datetime.datetime.now()))
#     print('')
#     DarwinCoreWriter().create_darwincore_archive(
#             datatype='Phytoplankton-JERICO', 
#             # dataset_dir='D:/arnold/4_sharkdata/notebooks/test_data/epi_nationella', 
#             dataset_dir='D:/arnold/4_sharkdata/notebooks/test_data/phytoplankton_jerico', 
#             national_data=True,
#             out_file_path='D:/arnold/4_sharkdata/notebooks/test_data/dwca-phytoplankton-jerico_TEST.zip', 
#             )
#     # JERICO-IFCB.
#     print('')
#     print('')
#     print('TEST: JERICO-IFCB. ' + str(datetime.datetime.now()))
#     print('')
#     DarwinCoreWriter().create_darwincore_archive(
#             datatype='Phytoplankton-JERICO-IFCB', 
#             # dataset_dir='D:/arnold/4_sharkdata/notebooks/test_data/epi_nationella', 
#             dataset_dir='D:/arnold/4_sharkdata/notebooks/test_data/phytoplankton_jerico', 
#             national_data=True,
#             out_file_path='D:/arnold/4_sharkdata/notebooks/test_data/dwca-phytoplankton-jerico-ifcb_TEST.zip', 
#             )
 
    # Greyseal.
    print('')
    print('')
    print('TEST: Greyseal. ' + str(datetime.datetime.now()))
    print('')
    DarwinCoreWriter().create_darwincore_archive(
            datatype='GreySeal', 
            # dataset_dir='D:/arnold/4_sharkdata/notebooks/test_data/epi_nationella', 
            dataset_dir='D:/arnold/4_sharkdata/notebooks/test_data/grey_harbour_ringed_seal', 
            national_data=True,
            out_file_path='D:/arnold/4_sharkdata/notebooks/test_data/dwca-greyseal-obis.zip', 
            )
#     # Harbourseal.
#     print('')
#     print('')
#     print('TEST: Harbourseal. ' + str(datetime.datetime.now()))
#     print('')
#     DarwinCoreWriter().create_darwincore_archive(
#             datatype='HarbourSeal', 
#             # dataset_dir='D:/arnold/4_sharkdata/notebooks/test_data/epi_nationella', 
#             dataset_dir='D:/arnold/4_sharkdata/notebooks/test_data/grey_harbour_ringed_seal', 
#             national_data=True,
#             out_file_path='D:/arnold/4_sharkdata/notebooks/test_data/dwca-harbourseal-obis.zip', 
#             )
#     # Ringedseal.
#     print('')
#     print('')
#     print('TEST: Ringedseal. ' + str(datetime.datetime.now()))
#     print('')
#     DarwinCoreWriter().create_darwincore_archive(
#             datatype='RingedSeal', 
#             # dataset_dir='D:/arnold/4_sharkdata/notebooks/test_data/epi_nationella', 
#             dataset_dir='D:/arnold/4_sharkdata/notebooks/test_data/grey_harbour_ringed_seal', 
#             national_data=True,
#             out_file_path='D:/arnold/4_sharkdata/notebooks/test_data/dwca-ringedseal-obis.zip', 
#             )
    
    
    print('')
    print('TEST: Finished. ' + str(datetime.datetime.now()))


