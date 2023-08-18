'''
Created on 2023-08-16

@author: wf
'''
import datetime
import pysrt
from nicesrt.geo import GeoPath
import re

class SRT:
    """
    Class to represent and manipulate SRT (SubRip Subtitle) data.
    
    Attributes:
        subtitles (list): List of parsed subtitles.
    """

    def __init__(self, subtitles, patterns=None, debug:bool=False):
        """
        Initializes the SRT object with the given subtitles and extraction patterns.
        """
        self.subtitles = subtitles
        self.debug = debug
        # Default patterns
        self.patterns = {
            'key_value': r'\[(\w+)\s*:\s*([\d.-]+)\]',
            'bracketed_value': r'(\w+)\(([\d.-]+),([\d.-]+)(?:,([\d.-]+))?\)'
        }

        if patterns:
            self.patterns.update(patterns)

    @classmethod
    def from_text(cls, text):
        """
        Class method to create an SRT object from a raw text string.
        """
        subtitles = pysrt.from_string(text)
        return cls(subtitles)

    def extract_value(self, index, key):
        """
        Extracts the value for a given key from the subtitle at the specified index.
        """
        result = None
        if index < len(self.subtitles):
            text = self.subtitles[index].text
            
            # Search using the key-value pattern
            matches = re.findall(self.patterns['key_value'], text)
            for k, v in matches:
                if k == key:
                    return v

            # Search using the bracketed value pattern
            matches = re.findall(self.patterns['bracketed_value'], text)
            for k, v1, v2, _ in matches:
                if k in ["GPS"] and key == "latitude":
                    return v2
                elif k in ["GPS"] and key == "longitude":
                    return v1

        return result
    
    def extract_date(self, index):
        """
        Extracts the date from the subtitle at the specified index.
        """
        if index < len(self.subtitles):
            # Define patterns for different date formats
            patterns = [
                (r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})', '%Y-%m-%d %H:%M:%S.%f'),
                (r'(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})', '%Y.%m.%d %H:%M:%S')
            ]
            
            text = self.subtitles[index].text
            result=None
            for pattern, fmt in patterns:
                match = re.search(pattern, text)
                if match:
                    date_str = match.group(1)
                    result= datetime.datetime.strptime(date_str, fmt)
            return result
        
    def as_geopath(self) -> GeoPath:
        """
        Converts the SRT object into a GeoPath object by extracting latitudes and longitudes.
        """
        geo_path = GeoPath()
        
        for index in range(len(self.subtitles)):
            try:
                lat_str = self.extract_value(index, "latitude")
                lon_str = self.extract_value(index, "longitude")
                
                # If both latitude and longitude are present, add them to the geo path
                if lat_str is not None and lon_str is not None:
                    lat = float(lat_str)
                    lon = float(lon_str)
                    geo_path.add_point(lat, lon)
            except BaseException as ex:
                if self.debug:
                    print(ex)
                pass

        return geo_path

        
