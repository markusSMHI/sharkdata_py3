#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import datetime
import pathlib
import shutil

from . import darwincore_utils
from . import darwincore_meta_xml
from . import darwincore_eml_xml

class DarwinCoreZip(object):
    """ """
    def __init__(self, dwca_file_path, 
                encoding='utf-8'):
        """ """
        self.dwca_file_path = dwca_file_path
        self.dwca_tmp_dir = None
        self.encoding = encoding
    
    def create_tmp_dir(self):
        """ """
        # Create tmp dir.
        target_zip_path = pathlib.Path(self.dwca_file_path).parents[0] # Parent dir.
        self.dwca_tmp_dir = pathlib.Path(target_zip_path.as_posix(), 'TMP_DarwinCore')
        if not self.dwca_tmp_dir.exists():
            self.dwca_tmp_dir.mkdir()
        else:
            # Remove content.
            self. remove_tmp_files()
    
    def remove_tmp_files(self):
        """ """
        try:
            # Remove used files first.
            for file_name in ['event.txt', 'occurrence.txt', 'extendedmeasurementorfact.txt', 
                              'meta.xml', 'eml.xml']:         
                file_path = pathlib.Path(self.dwca_tmp_dir, file_name)
                if file_path.exists():
                    file_path.unlink()
        except Exception as e:
            print('DEBUG: Failed to remove TMP_DarwinCore files: ' + str(e))
    
    def remove_tmp_dir(self):
        """ """
        try:
            self. remove_tmp_files()
            pathlib.Path(self.dwca_tmp_dir).rmdir()
        except Exception as e:
            print('DEBUG: Failed to remove TMP_DarwinCore dir: ' + str(e))
    
    def write_event_header(self, header):
        """ """
        if self.dwca_tmp_dir:
            file_path = pathlib.Path(self.dwca_tmp_dir, 'event.txt')
            with file_path.open('w', encoding=self.encoding, newline='\r\n') as file_w:
                file_w.write('\t'.join(header) + '\n')
    
    def write_event_rows(self, rows):
        """ """
        if self.dwca_tmp_dir:
            file_path = pathlib.Path(self.dwca_tmp_dir, 'event.txt')
            with file_path.open('a', encoding=self.encoding) as file_w:
                for row in rows:
                    file_w.write('\t'.join(row) + '\n')
    
    def write_occurrence_header(self, header):
        """ """
        if self.dwca_tmp_dir:
            file_path = pathlib.Path(self.dwca_tmp_dir, 'occurrence.txt')
            with file_path.open('w', encoding=self.encoding, newline='\r\n') as file_w:
                file_w.write('\t'.join(header) + '\n')
    
    def write_occurrence_rows(self, rows):
        """ """
        if self.dwca_tmp_dir:
            file_path = pathlib.Path(self.dwca_tmp_dir, 'occurrence.txt')
            with file_path.open('a', encoding=self.encoding) as file_w:
                for row in rows:
                    file_w.write('\t'.join(row) + '\n')
    
    def write_measurementorfact_header(self, header):
        """ """
        if self.dwca_tmp_dir:
            file_path = pathlib.Path(self.dwca_tmp_dir, 'extendedmeasurementorfact.txt')
            #
            with file_path.open('w', encoding=self.encoding, newline='\r\n') as file_w:
                file_w.write('\t'.join(header) + '\n')
    
    def write_measurementorfact_rows(self, rows):
        """ """
        if self.dwca_tmp_dir:
            file_path = pathlib.Path(self.dwca_tmp_dir, 'extendedmeasurementorfact.txt')
            with file_path.open('a', encoding=self.encoding) as file_w:
                for row in rows:
                    file_w.write('\t'.join(row) + '\n')
    
    def write_dwca_eml(self, eml_xml_content):
        """ """
        if self.dwca_tmp_dir:
            file_path = pathlib.Path(self.dwca_tmp_dir, 'eml.xml')
            with file_path.open('a', encoding=self.encoding) as file_w:
                for row in eml_xml_content:
                    file_w.write(row + '\n')
    
    def write_dwca_meta(self, dwca_meta_xml_rows):
        """ """
        if self.dwca_tmp_dir:
            file_path = pathlib.Path(self.dwca_tmp_dir, 'meta.xml')
#             with file_path.open('a', encoding=self.encoding) as file_w:
#                 file_w.write('\r\n'.join(dwca_meta_xml_rows).encode('utf-8'))
            with file_path.open('a', encoding=self.encoding) as file_w:
                for row in dwca_meta_xml_rows:
                    file_w.write(row + '\n')
    
    def create_darwingcore_zip_file(self, out_file_path='dwca_tmp.zip'): 
        """ """
        shutil.make_archive(out_file_path.replace('.zip', ''), 'zip', self.dwca_tmp_dir.as_posix())
    