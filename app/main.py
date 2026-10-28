
from fastapi import FastAPI
from app.api.devices import router as devices_router
from app.api.homes import router as homes_router

app = FastAPI(
    title="Home Energy Management System API",
    description="API for managing home energy devices and optimizing energy use.",
    version="0.1.0",
)
app.include_router(devices_router)
app.include_router(homes_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
