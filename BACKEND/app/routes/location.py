from fastapi import APIRouter
from global_land_mask import globe
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path


router = APIRouter()


MARINE_DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "geodata"
    / "ne_50m_geography_marine_polys.shp"
)


marine_areas = gpd.read_file(MARINE_DATA_PATH)


@router.get("/location")
def get_location(latitude: float, longitude: float):

    if latitude < -90 or latitude > 90:
        return {
            "status": "error",
            "message": "Invalid latitude"
        }

    if longitude < -180 or longitude > 180:
        return {
            "status": "error",
            "message": "Invalid longitude"
        }

    if globe.is_land(latitude, longitude):

        environment = "land"
        marine_region = None

    else:

        environment = "ocean"

        point = Point(longitude, latitude)

        matches = marine_areas[
            marine_areas.geometry.contains(point)
        ]

        if not matches.empty:

            if "name" in marine_areas.columns:
                marine_region = matches.iloc[0]["name"]

            elif "name_en" in marine_areas.columns:
                marine_region = matches.iloc[0]["name_en"]

            else:
                marine_region = "Marine region"

        else:
            marine_region = "Open Ocean"

    return {
        "status": "success",
        "latitude": latitude,
        "longitude": longitude,
        "environment": environment,
        "marine_region": marine_region,
        "message": "Location information retrieved successfully"
    }