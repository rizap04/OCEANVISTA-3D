from fastapi import APIRouter
from global_land_mask import globe

router = APIRouter()


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
        marine_region = "Open Ocean"

    return {
        "status": "success",
        "latitude": latitude,
        "longitude": longitude,
        "environment": environment,
        "marine_region": marine_region,
        "message": "Location information retrieved successfully"
    }