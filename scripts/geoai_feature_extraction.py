import geopandas as gpd
import rasterio
import pandas as pd
from rasterio.sample import sample_gen


def extract_raster_values(vector_path: str, raster_path: str, output_path: str) -> None:
    points = gpd.read_file(vector_path)
    raster = rasterio.open(raster_path)

    coords = [(x, y) for x, y in zip(points.geometry.x, points.geometry.y)]
    values = [val[0] for val in sample_gen(raster, coords)]

    points["elevation"] = values
    points.drop(columns="geometry").to_csv(output_path, index=False)

    print("Feature extraction complete. Dataset exported.")


if __name__ == "__main__":
    vector_file = "data/sample_points.geojson"
    raster_file = "data/sample_dem.tif"
    output_file = "outputs/ml_ready_dataset.csv"

    extract_raster_values(vector_file, raster_file, output_file)