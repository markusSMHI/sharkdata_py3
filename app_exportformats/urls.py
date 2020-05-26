#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-present SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from django.urls import path
import app_exportformats.views

urlpatterns = [
    path('', app_exportformats.views.listExportFiles),
    path('list/', app_exportformats.views.listExportFiles),
    path('list.json/', app_exportformats.views.listExportFilesJson),
    #
    path('table/', app_exportformats.views.tableExportFilesText),
    path('table.txt/', app_exportformats.views.tableExportFilesText),
    path('table.json/', app_exportformats.views.tableExportFilesJson),
    #
    path('ices_harvest.xml/', app_exportformats.views.icesHarvestXml),
#     path('ices_harvest.xml', app_exportformats.views.icesHarvestXml),
    #
    path('delete/<str:export_name>/', app_exportformats.views.deleteExportFile),
    # 
    path('<str:export_name>.xml/', app_exportformats.views.IcesXml),
    path('<str:export_name>_log.txt/', app_exportformats.views.IcesXmlLog),
]
