import numpy as np
import pandas as pd
import pyproj
import rasterio
import requests
from rasterio.enums import Resampling

# Funktion zur Umwandlung von WGS84-Koordinaten in LV95
transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:2056", always_xy=True)


def transform_wgs84_to_lv95(lon, lat):
    return transformer.transform(lon, lat)


# Funktion zur Bestimmung der passenden GeoTIFF-Datei
def find_matching_geotiff(csv_file, lv95_x, lv95_y):
    df = pd.read_csv(csv_file, header=None)
    for url in df[0]:
        if str(int(lv95_x // 1000)) in url and str(int(lv95_y // 1000)) in url:
            return url
    return None


# Funktion zum Herunterladen der GeoTIFF-Datei
def download_geotiff(url, output_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return output_path
    return None


# Funktion zur Berechnung der Hangneigung
def calculate_slope(geotiff_path, lv95_x, lv95_y):
    with rasterio.open(geotiff_path) as dataset:
        # Transformiere die LV95-Koordinaten in Pixel-Koordinaten
        row, col = dataset.index(lv95_x, lv95_y)

        # Lese die Höhenwerte um den Punkt
        window = ((row - 1, row + 2), (col - 1, col + 2))
        elevation = dataset.read(1, window=window, resampling=Resampling.bilinear)

        # Berechne den Gradient mit numpy
        x_grad, y_grad = np.gradient(elevation)
        slope = np.sqrt(x_grad[1, 1] ** 2 + y_grad[1, 1] ** 2)
        return np.degrees(np.arctan(slope))


# Beispielkoordinaten
wgs84_lat, wgs84_lon = 46.754479, 8.040906
lv95_x, lv95_y = transform_wgs84_to_lv95(wgs84_lon, wgs84_lat)

print(f"LV95-Koordinaten: {lv95_x}, {lv95_y}")

# CSV-Dateipfad
csv_file = "ch.swisstopo.swissalti3d-sdgpbP5J.csv"
geotiff_url = find_matching_geotiff(csv_file, lv95_x, lv95_y)

if geotiff_url:
    geotiff_path = "swissalti3d.tif"
    downloaded_file = download_geotiff(geotiff_url, geotiff_path)

    if downloaded_file:
        slope = calculate_slope(downloaded_file, lv95_x, lv95_y)
        print(f"Hangneigung an ({wgs84_lat}, {wgs84_lon}): {slope:.2f} Grad")
    else:
        print("Fehler beim Herunterladen der GeoTIFF-Datei.")
else:
    print("Keine passende GeoTIFF-Datei gefunden.")
