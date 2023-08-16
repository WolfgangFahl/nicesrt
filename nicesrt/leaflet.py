'''
https://github.com/zauberzeug/nicegui/blob/main/examples/map/leaflet.py

@author: rodja
'''
from typing import Tuple,List

from nicegui import ui


class leaflet(ui.element, component='leaflet.js'):

    def __init__(self) -> None:
        super().__init__()
        ui.add_head_html('<link href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css" rel="stylesheet"/>')
        ui.add_head_html('<script src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js"></script>')

    def set_location(self, location: Tuple[float, float]) -> None:
        self.run_method('set_location', location[0], location[1])
        
    def draw_path(self, path: List[Tuple[float, float]]) -> None:
        """Draw a path on the map based on list of lat-long tuples."""
        self.run_method('draw_path', path)