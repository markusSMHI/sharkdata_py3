#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-present SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from django.urls import path
import app_speciesobs.views

urlpatterns = [
    # HTML pages.
    path('', app_speciesobs.views.listSpeciesObs),
    path('list/', app_speciesobs.views.listSpeciesObs),
    path('table/', app_speciesobs.views.tableSpeciesObsText),
    
    # Text and JSON.
    path('table.txt/', app_speciesobs.views.tableSpeciesObsText),
    path('table.json/', app_speciesobs.views.tableSpeciesObsJson),
    
#     # Positions.
#     path('positions.kml/', app_speciesobs.views.positionsKml),
#     path('year_info.kml/', app_speciesobs.views.yearInfoKml),
#     path('map/', app_speciesobs.views.mapOpenlayers),
]
