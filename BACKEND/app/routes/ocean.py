from fastapi import APIRouter
from app.services.ocean_service import (
    get_nearest_ocean_data,
    load_ocean_data
)

router = APIRouter()


@router.get("/ocean-data")
def get_ocean_data(latitude: float, longitude: float):

    ocean_data = get_nearest_ocean_data(latitude, longitude)

    return {
        "latitude": float(ocean_data.latitude.values),
        "longitude": float(ocean_data.longitude.values),

        "temperature":
            ocean_data["temperature"].values.tolist(),

        "salinity":
            ocean_data["salinity"].values.tolist(),

        "depth":
            ocean_data["depth"].values.tolist()
    }


@router.get("/ocean-grid")
def get_ocean_grid():

    ocean_data = load_ocean_data()

    return {
        "latitude":
            ocean_data["latitude"].values.tolist(),

        "longitude":
            ocean_data["longitude"].values.tolist(),

        "depth":
            ocean_data["depth"].values.tolist(),

        "temperature":
            ocean_data["temperature"].values.tolist(),

        "salinity":
            ocean_data["salinity"].values.tolist()
    }