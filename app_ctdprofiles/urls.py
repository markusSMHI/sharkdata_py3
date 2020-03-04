#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-present SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from django.conf.urls import url
import app_ctdprofiles.views

urlpatterns = [
    url(r'^$', app_ctdprofiles.views.listCtdProfiles),
    url(r'^list/', app_ctdprofiles.views.listCtdProfiles),
    url(r'^list.json', app_ctdprofiles.views.listCtdProfilesJson),
    #
    url(r'^map/', app_ctdprofiles.views.viewTestMap),
    url(r'^plot/', app_ctdprofiles.views.viewTestPlot),
]
