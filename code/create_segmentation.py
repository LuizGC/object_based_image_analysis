import os
from osgeo import gdal
import numpy as np
from skimage.segmentation import felzenszwalb 

gdal.AllRegister()

dict_raster = None

def setup_dict_raster(gtif):
	global dict_raster
	if (dict_raster == None):
		dict_raster = {
			'rows': gtif.RasterYSize,
			'cols': gtif.RasterXSize,
			'driver': gtif.GetDriver(),
			'geoTransform': gtif.GetGeoTransform(),
			'projection': gtif.GetProjection()
		}

def get_array_data(gtif):
	bands_data_temp = []
	for band in range( gtif.RasterCount ):
		band += 1
		band_dataset = gtif.GetRasterBand(band)
		bands_data_temp.append(band_dataset.ReadAsArray())
	return bands_data_temp

TILES_PATH = 'tiles/'
segments_path = os.path.join(TILES_PATH, 'segments.tif')
if os.path.exists(segments_path):
	os.remove(segments_path)
bands_data = []
n_bands = 0
for file in os.listdir(TILES_PATH):
	if file.endswith(".tif"):
		path = os.path.join(TILES_PATH, file)
		raster_dataset = gdal.Open(path, gdal.GA_ReadOnly)
		setup_dict_raster(raster_dataset)
		for b in get_array_data(raster_dataset):
			n_bands = n_bands+1
			bands_data.append(b) 

bands_data = np.dstack(b for b in bands_data)

band_segmentation = []
for i in range(n_bands):
    band_segmentation.append(felzenszwalb(bands_data[:, :, i], scale=15, sigma=0.25, min_size=4))

const = [b.max() + 1 for b in band_segmentation]
segmentation = band_segmentation[0]
for i, s in enumerate(band_segmentation[1:]):
    segmentation += s * np.prod(const[:i+1])
_, labels = np.unique(segmentation, return_inverse=True)
segments_felz = labels.reshape(bands_data.shape[:2])
	
segments = segments_felz
segment_ids = np.unique(segments)
print("Felzenszwalb segmentation. %i segments." % len(segment_ids))

outDs = dict_raster['driver'].Create(segments_path, dict_raster['cols'], dict_raster['rows'], 1, gdal.GDT_Int32)

outBand = outDs.GetRasterBand(1)

outBand.WriteArray(segments, 0, 0)
outBand.FlushCache()
#outBand.SetNoDataValue(0)

outDs.SetGeoTransform(dict_raster['geoTransform'])
outDs.SetProjection(dict_raster['projection'])
print('fim')