#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from django.conf.urls import url
import app_sharkdataadmin.views

urlpatterns = [
    url(r'^$', app_sharkdataadmin.views.sharkDataAdmin),
    #
    url(r'^update_datasets_and_resources/', app_sharkdataadmin.views.updateDatasetsAndResources),
    #
    url(r'^delete_dwca_exportfiles/', app_sharkdataadmin.views.deleteDwcaExportFiles),
    url(r'^generate_dwca_exportfiles/', app_sharkdataadmin.views.generateDwcaExportFiles),
    #
    url(r'^generate_ices_xml_exportfiles/', app_sharkdataadmin.views.generateIcesXmlExportFiles),
    url(r'^validate_ices_xml_exportfiles/', app_sharkdataadmin.views.validateIcesXmlExportFiles),
    url(r'^delete_ices_xml_exportfiles/', app_sharkdataadmin.views.deleteIcesXmlExportFiles),
    #
    url(r'^speciesobs_update/', app_sharkdataadmin.views.updateSpeciesObs),
    url(r'^speciesobs_cleanup/', app_sharkdataadmin.views.cleanUpSpeciesObs),
    #
#     url(r'^view_log/(?P<log_id>\d+)/', app_sharkdataadmin.views.viewLog),
    url(r'^view_log/(?P<file_stem>[\w\-\_]+)/$', app_sharkdataadmin.views.viewLog),

]
