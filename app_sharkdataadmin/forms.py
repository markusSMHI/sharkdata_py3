#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from datetime import date
from django import forms

# class ImportDatasetForm(forms.Form):
#     """ """
#     import_file = forms.FileField(label="Select a SHARK archive file")
#     user = forms.CharField(label="User")
#     password = forms.CharField(label="Password", widget=forms.PasswordInput())

class DeleteAllDatasetsForm(forms.Form):
    """ Datasets. """
    delete_ftp = forms.BooleanField(label='Remove from FTP', required = False, initial = False)
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class LoadAllDatasetsForm(forms.Form):
    """ Datasets. """
#     update_metadata = forms.BooleanField(label='Update metadata', required = False, initial = False)
#     generate_archives = forms.BooleanField(label='Generate archives', required = False, initial = False)
    delete_old_ftp_versions = forms.BooleanField(label='Delete old versions', required = False, initial = False)
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class GenerateArchivesForm(forms.Form):
    """ Datasets. """
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class DeleteAllResourcesForm(forms.Form):
    """ resources. """
    delete_ftp = forms.BooleanField(label='Remove from FTP', required = False, initial = False)
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class LoadAllResourcesForm(forms.Form):
    """ resources. """
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class DeleteDwcaExportFilesForm(forms.Form):
    """ DarwinCore-Archive files. """
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class GenerateDwcaExportFilesForm(forms.Form):
    """ DarwinCore-Archive files. """
    last_year = date.today().year - 1
    status_for_monitoring_type = (
        ('NAT', 'NAT'),
        ('REG', 'REG'),
        ('Other', 'Other'),
        )
    #
    phytobenthos = forms.BooleanField(label='Phytobenthos', required = False, initial = True)
    phytoplankton = forms.BooleanField(label='Phytoplankton', required = False, initial = True)
    zoobenthos = forms.BooleanField(label='Zoobenthos', required = False, initial = True)
    zooplankton = forms.BooleanField(label='Zooplankton', required = False, initial = True)
#     year_from = forms.CharField(initial = last_year)
#     year_to = forms.CharField(initial = last_year)
    
    
    year_from = forms.CharField(initial = last_year-1)
    year_to = forms.CharField(initial = last_year-1)
    
#     year_from = forms.CharField(initial = '2008')
#     year_to = forms.CharField(initial = '2008')
    
    
    
    monitoring_type = forms.ChoiceField(choices=status_for_monitoring_type)
    #
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class DeleteIcesXmlExportFilesForm(forms.Form):
    """ ICES-XML files. """
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class GenerateIcesXmlExportFilesForm(forms.Form):
    """ ICES XML. """
    last_year = date.today().year - 1
    status_for_ices = (
        ('Not checked', 'Not checked'),
        ('Checked by DC', 'Checked by DC'),
        ('Test', 'Test'),
        )
    #
    phytobenthos = forms.BooleanField(label='Phytobenthos', required = False, initial = True)
    phytoplankton = forms.BooleanField(label='Phytoplankton', required = False, initial = True)
    zoobenthos = forms.BooleanField(label='Zoobenthos', required = False, initial = True)
    zooplankton = forms.BooleanField(label='Zooplankton', required = False, initial = True)
    year_from = forms.CharField(initial = last_year)
    year_to = forms.CharField(initial = last_year)
    status = forms.ChoiceField(choices=status_for_ices)
#     approved_by_dc = forms.BooleanField(label='Approved (DC)', required = False, initial = False)
    #
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class ValidateIcesXmlForm(forms.Form):
    """ ICES XML. """
    #
    phytobenthos = forms.BooleanField(label='Phytobenthos', required = False, initial = True)
    phytoplankton = forms.BooleanField(label='Phytoplankton', required = False, initial = True)
    zoobenthos = forms.BooleanField(label='Zoobenthos', required = False, initial = True)
    zooplankton = forms.BooleanField(label='Zooplankton', required = False, initial = True)
    #
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class UpdateSpeciesObsForm(forms.Form):
    """ Species observations. """
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class CleanUpSpeciesObsForm(forms.Form):
    """ Species observations. """
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
