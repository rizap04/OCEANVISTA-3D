import xarray as xr
import numpy as np

latitudes = [18.0, 18.5]
longitudes = [73.0, 73.5]
depths = [0, 50, 100]

temperature = np.array([
    [[26.0, 24.0, 22.0], [26.5, 24.5, 22.5]],
    [[27.0, 25.0, 23.0], [27.5, 25.5, 23.5]]
])

salinity = np.array([
    [[35.0, 35.2, 35.4], [35.1, 35.3, 35.5]],
    [[35.0, 35.2, 35.4], [35.1, 35.3, 35.5]]
])

ocean_data = xr.Dataset(
    {
        "temperature": (["latitude", "longitude", "depth"], temperature),
        "salinity": (["latitude", "longitude", "depth"], salinity)
    },
    coords={
        "latitude": latitudes,
        "longitude": longitudes,
        "depth": depths
    }
)

print(ocean_data)
