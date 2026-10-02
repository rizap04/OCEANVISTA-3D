from fastapi import APIRouter
from app.services.ocean_service import (
    get_nearest_ocean_data,
    load_ocean_data
)
import numpy as np


router = APIRouter()


def clean_values(values):
    """
    Convert NaN values into None
    so they can be sent safely as JSON.
    """

    arr = np.asarray(values, dtype=float)

    return np.where(
        np.isnan(arr),
        None,
        arr
    ).tolist()


def sample_indices(size, maximum=20):
    """
    Select evenly spaced indices from a dimension.

    This keeps the 3D visualization lightweight
    instead of sending the complete raw grid
    to the browser.
    """

    if size <= maximum:
        return np.arange(size)

    return np.linspace(
        0,
        size - 1,
        maximum,
        dtype=int
    )


@router.get("/ocean-data")
def get_ocean_data(
    latitude: float,
    longitude: float
):

    ocean_data = get_nearest_ocean_data(
        latitude,
        longitude
    )

    return {
        "latitude": float(
            ocean_data.latitude.values
        ),

        "longitude": float(
            ocean_data.longitude.values
        ),

        "temperature": clean_values(
            ocean_data["temperature"].values
        ),

        "depth": (
            ocean_data["depth"]
            .values
            .tolist()
        )
    }


@router.get("/ocean-grid")
def get_ocean_grid():

    ocean_data = load_ocean_data()

    # -----------------------------------------
    # Create a lightweight visualization grid
    # -----------------------------------------

    latitude_indices = sample_indices(
        ocean_data.sizes["latitude"],
        20
    )

    longitude_indices = sample_indices(
        ocean_data.sizes["longitude"],
        20
    )

    depth_indices = sample_indices(
        ocean_data.sizes["depth"],
        20
    )

    # -----------------------------------------
    # Select only the required points
    # -----------------------------------------

    sampled_data = ocean_data.isel(
        latitude=latitude_indices,
        longitude=longitude_indices,
        depth=depth_indices
    )

    # -----------------------------------------
    # Send compact grid to frontend
    # -----------------------------------------

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