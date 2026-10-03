from fastapi import APIRouter
from app.services.ocean_service import get_ocean_data
import numpy as np


router = APIRouter()


# --------------------------------------------------
# Convert NaN values to None for JSON
# --------------------------------------------------

def clean_values(values):

    arr = np.asarray(values, dtype=float)

    return np.where(
        np.isnan(arr),
        None,
        arr
    ).tolist()


# --------------------------------------------------
# Selected location temperature profile
# --------------------------------------------------

@router.get("/ocean-data")
def get_ocean_data_endpoint(
    latitude: float,
    longitude: float
):

    ocean_data = get_ocean_data(
        round(latitude, 2),
        round(longitude, 2)
    )

    # Find nearest grid cell
    selected = ocean_data.sel(
        latitude=latitude,
        longitude=longitude,
        method="nearest"
    )

    return {

        "latitude": float(
            selected.latitude.values
        ),

        "longitude": float(
            selected.longitude.values
        ),

        "temperature": clean_values(
            selected["temperature"].values
        ),

        "depth": (
            selected["depth"]
            .values
            .tolist()
        )

    }


# --------------------------------------------------
# Dynamic 3D ocean grid
# --------------------------------------------------

@router.get("/ocean-grid")
def get_ocean_grid(
    latitude: float,
    longitude: float
):

    ocean_data = get_ocean_data(
        round(latitude, 2),
        round(longitude, 2)
    )

    # ----------------------------------------------
    # Select a lightweight local grid
    # ----------------------------------------------

    latitude_indices = np.linspace(
        0,
        ocean_data.sizes["latitude"] - 1,
        min(7, ocean_data.sizes["latitude"]),
        dtype=int
    )

    longitude_indices = np.linspace(
        0,
        ocean_data.sizes["longitude"] - 1,
        min(7, ocean_data.sizes["longitude"]),
        dtype=int
    )

    depth_indices = np.linspace(
        0,
        ocean_data.sizes["depth"] - 1,
        min(15, ocean_data.sizes["depth"]),
        dtype=int
    )

    sampled_data = ocean_data.isel(
        latitude=latitude_indices,
        longitude=longitude_indices,
        depth=depth_indices
    )

    return {

        "latitude":
            sampled_data["latitude"]
            .values
            .tolist(),

        "longitude":
            sampled_data["longitude"]
            .values
            .tolist(),

        "depth":
            sampled_data["depth"]
            .values
            .tolist(),

        "temperature":
            clean_values(
                sampled_data["temperature"].values
            )

    }