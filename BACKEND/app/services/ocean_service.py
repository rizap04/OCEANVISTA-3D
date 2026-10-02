import xarray as xr
from pathlib import Path
from functools import lru_cache

DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m_1790868104467.nc"
)


@lru_cache(maxsize=1)
def load_ocean_data():
    ocean_data = xr.open_dataset(DATA_FILE)
    ocean_data = ocean_data.squeeze("time")
    ocean_data = ocean_data.rename({"thetao": "temperature"})
    ocean_data = ocean_data.transpose("latitude", "longitude", "depth")
    return ocean_data.load()


def get_nearest_ocean_data(latitude, longitude):
    ocean_data = load_ocean_data()
    return ocean_data.sel(
        latitude=latitude,
        longitude=longitude,
        method="nearest"
    )