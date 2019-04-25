#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import codecs
from django.conf import settings
import sharkdata_core

class IcesHarvestXml(object):
    """ """
    def __init__(self):
        """ """

    def approved_icex_exports_listed_in_xml(self, approved_export_file_list,
                                                  create_date_filter, 
                                                  monitoring_year_filter,
                                                  datatype_filter):
        """ XML formatted listing of approved files. XML instead of JSON or text table, is demanded by ICES. """
        
        xml_message = []
        
        xml_message.append("<?xml version='1.0' encoding='utf-8' standalone='no'?>")
        xml_message.append("<?xml-stylesheet type='text/xsl' href='metadata.xsl'?>")
        
        for item_dict in approved_export_file_list:
            
            if item_dict.get('approved', '') == 'True':
                
                export_file_name = item_dict.get('export_file_name', '')
                generated_datetime = item_dict.get('generated_datetime', '')
                if len(generated_datetime) >= 10:
                    generated_datetime = generated_datetime[:10]
                year = item_dict.get('year', '')
                datatype = item_dict.get('datatype', '')
                export_file_name = item_dict.get('export_file_name', '')
                
                # Datatype
                if datatype == 'Epibenthos': datatype = 'PB'
                if datatype == 'Phytobenthos': datatype = 'PB'
                if datatype == 'Phytoplankton': datatype = 'PP'
                if datatype == 'Zoobenthos': datatype = 'ZB'
                if datatype == 'Zooplankton': datatype = 'ZP'

                # Filter
                if create_date_filter:
                    if generated_datetime != create_date_filter:
                        continue
                if monitoring_year_filter:
                    if year != monitoring_year_filter:
                        continue
                if datatype_filter:
                    if datatype.upper() != datatype_filter.upper():
                        continue

                # Add to XML.                
                xml_message.append("<File_information xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='metadata.xsd'>")
                xml_message.append("    <ContactEmail>shark@smhi.se</ContactEmail>")
                xml_message.append("    <filename>" + export_file_name + "</filename>")
                xml_message.append("    <createdate>" + generated_datetime + "</createdate >")
                xml_message.append("    <MonitoringYear>" + year + "</MonitoringYear >")
                xml_message.append("    <DataType>" + datatype + "</DataType >")
                xml_message.append("    <URI>" + 'http://sharkdata.se/exportformats/' + export_file_name + "</URI>")
                xml_message.append("</File_information>")
            
        # print('\r\n'.join(xml_message))
        
        return '\r\n'.join(xml_message)


# Example from ICES:
# <?xml version='1.0' encoding='utf-8' standalone='no'?>
# <?xml-stylesheet type='text/xsl' href='metadata.xsl'?>
# <File_information xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='metadata.xsd'>
# <ContactEmail>carlos@ices.dk</ContactEmail> 
#  <filename>ICES-XML_SMHI_Zooplankton_2016.xml</SamplingInstitute> 
#  <createdate>07-09-2016</createdate > 
# <MonitoringYear>2016</MonitoringYear >
# <DataType>ZB</DataType >
# <modifiedDate>08-09-2017<modifiedDate>
# <URI>http://sharkdata.se/files/ ICES-XML_SMHI_Zooplankton_2016.xml</URI>
# </File_information>

#         test_data = [
#             {"status": "DATSU-failed", "format": "ICES-XML", "datatype": "Zooplankton", "export_name": "ICES-XML_SMHI_Zooplankton_2016", "export_file_name": "ICES-XML_SMHI_Zooplankton_2016.xml", "year": "2016", "approved": "False", "generated_datetime": "2017-09-28 13:27:03.037533+00:00"}, 
#             {"status": "DATSU-ok", "format": "ICES-XML", "datatype": "Epibenthos", "export_name": "ICES-XML_SMHI_Epibenthos_2016", "export_file_name": "ICES-XML_SMHI_Epibenthos_2016.xml", "year": "2016", "approved": "True", "generated_datetime": "2017-09-28 13:21:07.325069+00:00"}, 
#             {"status": "DATSU-ok", "format": "ICES-XML", "datatype": "Phytoplankton", "export_name": "ICES-XML_SMHI_Phytoplankton_2016", "export_file_name": "ICES-XML_SMHI_Phytoplankton_2016.xml", "year": "2016", "approved": "True", "generated_datetime": "2017-09-28 13:22:14.125343+00:00"}, 
#             {"status": "DATSU-ok", "format": "ICES-XML", "datatype": "Zoobenthos", "export_name": "ICES-XML_SMHI_Zoobenthos_2016", "export_file_name": "ICES-XML_SMHI_Zoobenthos_2016.xml", "year": "2016", "approved": "True", "generated_datetime": "2017-09-28 13:26:33.412435+00:00"}
#             ]
