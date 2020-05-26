#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-present SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from django.urls import path
import app_sharkdataadmin.views

urlpatterns = [
    path('', app_sharkdataadmin.views.sharkDataAdmin),
    #
    path('update_datasets_and_resources/', app_sharkdataadmin.views.updateDatasetsAndResources),
    path('update_datasets_and_resources/datasets_load_all/', app_sharkdataadmin.views.updateDatasetsAndResources),
    #
    path('delete_dwca_exportfiles/', app_sharkdataadmin.views.deleteDwcaExportFiles),
    path('delete_dwca_exportfiles/exportfiles_delete_all_dwca/', app_sharkdataadmin.views.deleteDwcaExportFiles),
    path('generate_dwca_exportfiles/', app_sharkdataadmin.views.generateDwcaExportFiles),
    path('generate_dwca_exportfiles/generate_dwca_exportfiles/', app_sharkdataadmin.views.generateDwcaExportFiles),
    #
    path('delete_ices_xml_exportfiles/', app_sharkdataadmin.views.deleteIcesXmlExportFiles),
    path('delete_ices_xml_exportfiles/delete_ices_xml_exportfiles/', app_sharkdataadmin.views.deleteIcesXmlExportFiles),
    path('generate_ices_xml_exportfiles/', app_sharkdataadmin.views.generateIcesXmlExportFiles),
    path('generate_ices_xml_exportfiles/generate_ices_xml_exportfiles/', app_sharkdataadmin.views.generateIcesXmlExportFiles),
    path('validate_ices_xml_exportfiles/', app_sharkdataadmin.views.validateIcesXmlExportFiles),
    path('validate_ices_xml_exportfiles/validate_ices_xml_exportfiles/', app_sharkdataadmin.views.validateIcesXmlExportFiles),
    #
    path('speciesobs_cleanup/', app_sharkdataadmin.views.cleanUpSpeciesObs),
    path('speciesobs_cleanup/speciesobs_cleanup/', app_sharkdataadmin.views.cleanUpSpeciesObs),
    path('speciesobs_update/', app_sharkdataadmin.views.updateSpeciesObs),
    path('speciesobs_update/speciesobs_update/', app_sharkdataadmin.views.updateSpeciesObs),
    #
#     path('view_log/<str:log_id>/', app_sharkdataadmin.views.viewLog),
    path('view_log/<str:file_stem>/', app_sharkdataadmin.views.viewLog),

]

