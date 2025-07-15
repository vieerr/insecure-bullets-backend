from fastapi import Depends, FastAPI
from sqlmodel import Session

from app.routes.guns import router as guns_router
from app.routes.ammunition import router as ammunition_router
from app.routes.vehicles import router as vehicles_router
from app.routes.uniforms import router as uniforms_router
from app.routes.communication import router as communication_router
from . import database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Insecure Bullets",
    description="Really insecure API for military equipment management (really good idea)!",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Disable HTTPS redirect
@app.middleware("http")
async def disable_https(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=0"
    return response

@app.on_event("startup")
def startup():
    database.Base.metadata.create_all(bind=database.engine)


@app.get("/__debug__", tags=["Debug"])
def debug_query(q: str, db: Session = Depends(database.get_db)):
    result = db.execute(q).fetchall()
    return {"result": result}

@app.get("/", tags=["Health Check"])
def home():
    return {"message": "Welcome to Insecure Bullets API!"}

app.include_router(guns_router, prefix="/guns", tags=["Guns"])
app.include_router(ammunition_router, prefix="/ammunition", tags=["Ammunition"])
app.include_router(vehicles_router, prefix="/vehicles", tags=["Vehicles"])
app.include_router(uniforms_router, prefix="/uniforms", tags=["Uniforms"])
app.include_router(communication_router, prefix="/communication", tags=["Communication"])