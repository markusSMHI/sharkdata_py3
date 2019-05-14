#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from datetime import date
from django import forms

class UpdateDatasetsAndResourcesForm(forms.Form):
    """ Datasets. """
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
    year_from = forms.CharField(initial = last_year)
    year_to = forms.CharField(initial = last_year)
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
    
    
    # last_year = 2012
    
    
    status_for_ices = (
        ('Not checked', 'Not checked'),
        ('Checked by DC', 'Checked by DC'),
        ('Test', 'Test'),
        )
    #
    phytobenthos = forms.BooleanField(label='Phytobenthos', required = False, initial = False)
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
