#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://sharkdata.se
# Copyright (c) 2018-present SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import datetime
import pathlib
import folium
import bokeh

# from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

from app_ctdprofiles import ctd_profile_plot

class CtdProfilesCore():
    """ """
    
    def __init__(self):
        """ """
    
    def createMap(self, 
                  lat_long_desc_table=[]):
        """ Plots positions on an interactive OpenStreetMap by using the folium library. """
        m = folium.Map([60.0, 15.0], zoom_start=5)
        test = folium.Html('<b>Hello world</b>', script=True)
        popup = folium.Popup(test, max_width=2650)
        
        # TEST DATA.
        if not lat_long_desc_table:
            lat_long_desc_table = [
                [55.6175, 14.8675, 'Svea-2019-1111'], 
#                 [60.0, 20.0, 'Svea-2019-1222'], 
#                 [60.0, 20.0, 'Svea-2019-1333'], 
#                 [60.0, 20.5, 'Svea-2019-1444'], 
                ]
        
        #
        for lat, long, desc in lat_long_desc_table:
            marker = folium.Marker([lat, long], popup=desc).add_to(m)
        
            
#         folium.RegularPolygonMarker(location=[57.0, 17.5], popup=popup).add_to(m)
    
        return m.get_root().render()


    def createPlot(self, path_zipfile, profile_name):
        """ Plots ... """
        
#         from bokeh.plotting import figure, show, output_file
#         from bokeh.sampledata.iris import flowers
#         
#         colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
#         colors = [colormap[x] for x in flowers['species']]
#         
#         p = figure(title = "Iris Morphology")
#         p.xaxis.axis_label = 'Petal Length'
#         p.yaxis.axis_label = 'Petal Width'
#         
#         p.circle(flowers["petal_length"], flowers["petal_width"],
#                  color=colors, fill_alpha=0.2, size=10)
#         
#         output_file("iris.html", title="iris.py example")
#         
# #         show(p)
#         
#         script, div = bokeh.components(p)
#     
#         return script, div


#         from bokeh.plotting import figure
#         from bokeh.resources import CDN
#         from bokeh.embed import file_html
#         
#         plot = figure()
#         plot.circle([1,2], [3,4])
#         
#         html = file_html(plot, CDN, "my plot")
# 
#         return html
    
    
        path_zipfile = 'D:/arnold/41_sharkdata_sharkdata_v2/sharkdata_ftp/datasets/SHARK_CTDprofile_2018_BAS_SMHI_version_2019-01-17.zip'
        profile_name = 'ctd_profile_SBE09_0745_20181209_1122_34_01_0173'
        
        rzip = ctd_profile_plot.ReadZipFile(path_zipfile, profile_name)
    
        parameter_list = ['PRES_CTD [dbar]', 'CNDC_CTD [S/m]', 'CNDC2_CTD [S/m]', 'SALT_CTD [psu (PSS-78)]',
                          'SALT2_CTD [psu (PSS-78)]', 'TEMP_CTD [°C (ITS-90)]', 'TEMP2_CTD [°C (ITS-90)]',
                          'DOXY_CTD [ml/l]', 'DOXY2_CTD [ml/l]', 'PAR_CTD [µE/(cm2 ·sec)]', 'CHLFLUO_CTD [mg/m3]',
                          'TURB_CTD [NTU]', 'PHYC_CTD [ppb]']
    
        data = rzip.get_data(parameter_list)
    
        profile = ctd_profile_plot.ProfilePlot(data, parameters=parameter_list)
        plot = profile.plot(x='TEMP_CTD [°C (ITS-90)]',
                            y='PRES_CTD [dbar]',
                            z='SALT_CTD [psu (PSS-78)]',
                            name=profile_name)

        html = file_html(plot, CDN, "my plot")
        return html

# # FOLIUM:
# def plot_positions_on_map(self, map_file_path=None):
# 
#         # Create name if not specified.
#         if map_file_path is None:
#             map_file_path=str(pathlib.Path(self.scanning_results_dir, 
#                                            'positions_map.html'))
#                 
#         # Remove rows with no position.
#         files_with_pos_df = pd.DataFrame(self.files_df)
#         files_with_pos_df.latlong_str.replace('', np.nan, inplace=True)
#         files_with_pos_df.dropna(subset=['latlong_str'], inplace=True) 
#         if len(files_with_pos_df) > 0:
#         
#             # Group by positions and count files at each position.
#             distinct_df = pd.DataFrame(
#                     {'file_count' : files_with_pos_df.groupby( ['latlong_str', 
#                                                                 'latitude_dd', 
#                                                                 'longitude_dd']).size()
#                     }).reset_index()
#             
#             # Add a column for description to be shown when hovering over point in map.
#             distinct_df['description'] = 'Pos: ' + distinct_df['latlong_str'] + \
#                                          ' Count: ' + distinct_df['file_count'].astype(str)
#             
#             # Use the mean value as center for the map.
#             center_lat = distinct_df.latitude_dd.mean()
#             center_long = distinct_df.longitude_dd.mean()
#             
#             # Create map object.
#             map_osm = folium.Map(location=[center_lat, center_long], zoom_start=8)
#             
#             # Loop over positions an create markers.
#             for long, lat, desc in zip(distinct_df.longitude_dd.values,
#                                      distinct_df.latitude_dd.values,
#                                      distinct_df.description.values):
#                 # The description column is used for popup messages.
#                 marker = folium.Marker([lat, long], popup=desc).add_to(map_osm)            
#             
#             # Write to html file.
#             map_osm.save(map_file_path)
#             if self.debug:
#                 print('Position map saved here: ', map_file_path)
#         else:
#             if self.debug:
#                 print('\n', 'Warning: Position map not created. Lat/long positions are missing.', '\n')


