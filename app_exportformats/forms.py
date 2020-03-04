#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-present SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from django import forms

class DeleteExportFileForm(forms.Form):
    """ """
#     delete_ftp = forms.BooleanField(label='Remove from FTP', required = False, initial = False)
    user = forms.CharField(label="User")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
