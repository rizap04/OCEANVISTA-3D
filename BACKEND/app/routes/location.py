from fastapi import APIRouter

router = APIRouter()


@router.get("/location")
def get_location(latitude: float, longitude: float):
    return {
        "latitude": latitude,
        "longitude": longitude,
        "message": "Ocean location received successfully"
    }