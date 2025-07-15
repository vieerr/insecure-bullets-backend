from fastapi import FastAPI

from app.routes.guns import router as guns_router
from app.routes.ammunition import router as ammunition_router
from app.routes.vehicles import router as vehicles_router
from app.routes.uniforms import router as uniforms_router
from app.routes.communication import router as communication_router

app = FastAPI(
    title="Insecure Bullets",
    description="Really insecure API for military equipment management (really good idea)!",
    version="1.0.0",
)

@app.get("/", tags=["Health Check"])
def home():
    return {"message": "Welcome to Insecure Bullets API!"}

app.include_router(guns_router, prefix="/guns", tags=["Guns"])
app.include_router(ammunition_router, prefix="/ammunition", tags=["Ammunition"])
app.include_router(vehicles_router, prefix="/vehicles", tags=["Vehicles"])
app.include_router(uniforms_router, prefix="/uniforms", tags=["Uniforms"])
app.include_router(communication_router, prefix="/communication", tags=["Communication"])