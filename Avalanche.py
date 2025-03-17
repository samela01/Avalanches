import rasterio
import numpy as np
import folium
import pandas as pd
from tkinter import Tk, Label, Button, OptionMenu, StringVar
from folium.plugins import Draw

# Funktion zum Laden der GeoTIFF-Dateien aus einer CSV-Datei
def load_tiff_paths(csv_file):
    df = pd.read_csv(csv_file, header=None)  # Annahme: Eine Spalte mit Pfaden
    return df[0].tolist()

# Funktion zum Laden eines Höhenmodells aus einer GeoTIFF-Datei
def load_dem(file_path):
    with rasterio.open(file_path) as dataset:
        dem = dataset.read(1)  # Erstes Band (Höhenwerte)
        transform = dataset.transform
    return dem, transform

# Funktion zur Berechnung der Hangneigung
def calculate_slope(dem):
    x_gradient, y_gradient = np.gradient(dem)
    slope = np.sqrt(x_gradient**2 + y_gradient**2)
    slope_degrees = np.degrees(np.arctan(slope))
    return slope_degrees

# Funktion zur Erstellung der interaktiven Karte
def create_map():
    m = folium.Map(location=[47.5, 11.0], zoom_start=10)
    Draw(export=True).add_to(m)
    return m

# GUI mit Tkinter für die Auswahl der Lawinenlage-Parameter
def create_gui():
    root = Tk()
    root.title("Strecke")

    Label(root, text="Temperatur").pack()
    temp_var = StringVar(root)
    temp_menu = OptionMenu(root, temp_var, "-10°C", "0°C", "+5°C")
    temp_menu.pack()

    Label(root, text="Schnee").pack()
    snow_var = StringVar(root)
    snow_menu = OptionMenu(root, snow_var, "wenig", "mittel", "viel")
    snow_menu.pack()

    Label(root, text="Warnstufe").pack()
    warn_var = StringVar(root)
    warn_menu = OptionMenu(root, warn_var, "1", "2", "3", "4", "5")
    warn_menu.pack()

    Button(root, text="Start", command=lambda: print("Analyse starten")).pack()
    root.mainloop()

# Hauptfunktion
def main():
    csv_file = "C:\\Users\\Administrator\\Documents\\Studienarbeit\\Avalanches\\ch.swisstopo.swissalti3d-zpOR9HnL.csv" 
    tiff_files = load_tiff_paths(csv_file)
    dem, transform = load_dem(tiff_files[0])
    slope = calculate_slope(dem)
    m = create_map()
    m.save("map.html")
    create_gui()
