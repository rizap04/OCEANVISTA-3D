import copernicusmarine
import xarray as xr
from functools import lru_cache
from pathlib import Path


# --------------------------------------------------
# Copernicus Marine Global Ocean Dataset
# --------------------------------------------------

DATASET_ID = "cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m"

DATA_FOLDER = Path("data")


# --------------------------------------------------
# Get ocean temperature for a selected location
# --------------------------------------------------

@lru_cache(maxsize=100)
def get_ocean_data(latitude, longitude):

    # Small area around the selected location
    margin = 0.25

    filename = f"ocean_{latitude}_{longitude}.nc"

    output_path = DATA_FOLDER / filename

    DATA_FOLDER.mkdir(exist_ok=True)

    # Download only the required area
    copernicusmarine.subset(
        dataset_id=DATASET_ID,

        variables=["thetao"],

        minimum_longitude=longitude - margin,
        maximum_longitude=longitude + margin,

        minimum_latitude=latitude - margin,
        maximum_latitude=latitude + margin,

        minimum_depth=0.5,
        maximum_depth=100,

        start_datetime="2026-10-01",
        end_datetime="2026-10-01",

        output_directory=str(DATA_FOLDER),

        output_filename=filename,

        overwrite=False
    )

    # Open the actual NetCDF file
    data = xr.open_dataset(
        output_path,
        engine="netcdf4"
    )

    # Remove time dimension
    data = data.squeeze("time")

    # Rename temperature variable
    data = data.rename(
        {
            "thetao": "temperature"
        }
    )

    return data


# --------------------------------------------------
# Find nearest ocean data
# --------------------------------------------------

def get_nearest_ocean_data(latitude, longitude):

    ocean_data = get_ocean_data(
        round(latitude, 2),
        round(longitude, 2)
    )

    return ocean_data.sel(
        latitude=latitude,
        longitude=longitude,
        method="nearest"
    )


# --------------------------------------------------
# Compatibility function
# --------------------------------------------------

def load_ocean_data():

    return get_ocean_data(
        18.0,
        72.0
    )