#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from django.conf.urls import url
import app_exportformats.views

urlpatterns = [
    url(r'^$', app_exportformats.views.listExportFiles),
    url(r'^list/', app_exportformats.views.listExportFiles),
    url(r'^list.json/', app_exportformats.views.listExportFilesJson),
    #
    url(r'^table/', app_exportformats.views.tableExportFilesText),
    url(r'^table.txt/', app_exportformats.views.tableExportFilesText),
    url(r'^table.json/', app_exportformats.views.tableExportFilesJson),
    #
    url(r'^ices_harvest.xml/', app_exportformats.views.icesHarvestXml),
    url(r'^ices_harvest.xml', app_exportformats.views.icesHarvestXml),
    #
    url(r'^delete/(?P<export_name>\S+)', app_exportformats.views.deleteExportFile),
    # 
    url(r'^(?P<export_name>\S+).xml', app_exportformats.views.IcesXml),
    url(r'^(?P<export_name>\S+)_log.txt', app_exportformats.views.IcesXmlLog),
]
