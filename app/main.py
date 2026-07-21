from contextlib import asynccontextmanager
from fastapi import FastAPI #type: ignore
from fastapi.middleware.cors import CORSMiddleware  #type: ignore

from app.api.health_router import ( router as health_router )
from app.api.vehicle_router import ( router as vehicle_router,)
from app.api.employee_router import ( router as employee_router)
from app.api.driver_router import (  router as driver_router,)
from app.api.complaint_router import ( router as complaint_router,)
from app.api.jobcard_router import ( router as jobcard_router )
from app.api.jobcard_part_router import ( router as jobcard_part_router )
from app.api.checklist_router import ( router as checklist_router )
from app.api.inspection_router import ( router as inspection_router )
from app.api.part_router import ( router as part_router )
from app.core.exception_handlers import ( register_exception_handlers,)
from app.api.audit_router import ( router as audit_router,)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FMS Started")
    yield
    print("FMS Stopped")

app = FastAPI(
    title="Fleet Management System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {
        "application": "Fleet Management System",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

register_exception_handlers(    app)

app.include_router(    vehicle_router)
app.include_router(    employee_router)
app.include_router(    driver_router)
app.include_router(    complaint_router)
app.include_router(    health_router)
app.include_router(    part_router)
app.include_router(    inspection_router)
app.include_router(    jobcard_router)
app.include_router(    jobcard_part_router)
app.include_router(    checklist_router)
app.include_router(    audit_router)
