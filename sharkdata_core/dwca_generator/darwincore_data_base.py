#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import datetime
import pytz

class DarwinCoreDataBase(object):
    """ """
    def __init__(self):
        """ Base class. """
        #
        self.worms_info_object = None

    def add_extra_fields(self, row_dict):
        """ Default implementation if not defined in subclass. """
        pass

    def create_extra_keys(self, row_dict):
        """ Default implementation if not defined in subclass. """
        pass

    def get_default_mapping(self):
        """ Default implementation if not defined in subclass. """
        return {}

    def _create_extra_key(self, row_dict, key_list):
        """ """
        key_string = ''
        try:
#            key_list = [str(row_dict.get(item, '')) for item in key_columns if row_dict.get(item, False)]
            value_list = []
            for (descr, key_column) in key_list:
                value = str(row_dict.get(key_column, '')) 
                if value:
#                    value_list.append(value + '(' + descr + ')')
                    value_list.append('"' + descr + '":"' + value.replace(',', '.') + '"')
            #
            key_string = ','.join(value_list)
        except:
            key_string = 'ERROR: Failed to generate key-string'
        # Replace swedish characters.
        key_string = key_string.replace('Å', 'A')
        key_string = key_string.replace('Ä', 'A')
        key_string = key_string.replace('Ö', 'O')
        key_string = key_string.replace('å', 'a')
        key_string = key_string.replace('ä', 'a')
        key_string = key_string.replace('ö', 'o')
        key_string = key_string.replace('µ', 'u')
        #
        return key_string
    

    def is_daylight_savings_time(self, date_str, zone_name='Europe/Stockholm'):
        """ Returns True if DST=Daylight Savings Time. """
        try:
            localtime = pytz.timezone(zone_name)
            datetime_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            localized_date = localtime.localize(datetime_date)
            return bool(localized_date.dst())
        except:
            return False
        
