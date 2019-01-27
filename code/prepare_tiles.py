import os
from osgeo import gdal

SENTINEL_TILES_PATH = 'sentinel-tiles/'
TILES_PATH = 'prepared-tiles/'
CUTLINE_LAYER_PATH= 'area_study/area.shp'

for file in os.listdir(SENTINEL_TILES_PATH):
    if file.endswith(".jp2"):
        input_path = os.path.join(SENTINEL_TILES_PATH, file)
        input_raster = gdal.Open(input_path, gdal.GA_ReadOnly)
        output_path = os.path.join(TILES_PATH, file.replace('jp2', 'tif'))
        if os.path.exists(output_path):
            os.remove(output_path)
        gdal.Warp(output_path, input_raster, dstSRS='EPSG:4326', cropToCutline=True, cutlineDSName=CUTLINE_LAYER_PATH)

