from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.location import router as location_router
from app.routes.ocean import router as ocean_router


app = FastAPI()


app.include_router(location_router)
app.include_router(ocean_router)


@app.get("/status")
def status():
    return {
        "status": "OCEANVISTA backend is running"
    }


app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)