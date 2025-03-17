from Avalanche import load_tiff_paths, load_dem, calculate_slope, create_map, create_gui

def main():
    csv_file = "C:\\Users\\Administrator\\Documents\\Studienarbeit\\Avalanches\\ch.swisstopo.swissalti3d.csv"  
    tiff_paths = load_tiff_paths(csv_file)
    
    for tiff_path in tiff_paths:
        dem, transform = load_dem(tiff_path)
        slope = calculate_slope(dem)
        print(f"Berechnete Hangneigung für {tiff_path}")
    
    map_object = create_map()
    map_object.save("map.html")
    
    create_gui()

if __name__ == "__main__":
    main()
# In this snippet, we import the functions from the Avalanche.py file and call them in the main function.














