from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Literal

import os
import sys
import secrets
import psycopg

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import crud

API_KEYS = {key.strip() for key in os.environ.get("READ_API_KEYS", "").split(",") if key.strip()}

API_VERSION = "1.0"

app = FastAPI(
    title="DinoBase API",
    description="A beginner-friendly REST API containing information about Prehistoric Animal.",
    version=API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#DATA MODEL
class PrehistoricCreature(BaseModel):
    id: int
    name: str = Field(min_length=1)
    scientific_name: str = Field(min_length=1)
    period: Literal["Cambrian", "Ordovician", "Silurian", "Devonian", "Carboniferous", "Permian", "Triassic", "Jurassic", "Cretaceous", "Paleogene", "Neogene", "Quaternary"]
    diet: Literal["Carnivore", "Herbivore", "Omnivore", "Piscivore", "Insectivore", "Filter Feeder"]
    family: str = Field(min_length=1)
    type: str = Field(min_length=1)
    defence: str = Field(min_length=1)
    location: str = Field(min_length=1)
    discovered: str = Field(min_length=1)
    life_span: str = Field(min_length=1)
    habitat: Literal["Terrestrial", "Amphibious", "Aquatic", "Aerial", "Fossorial", "Arboreal"]
    weight: str = Field(min_length=1)
    height: str = Field(min_length=1)
    extinction: str = Field(min_length=1)

# Allowed values for the create and update models and the list filters
Period = Literal["Cambrian", "Ordovician", "Silurian", "Devonian", "Carboniferous", "Permian", "Triassic", "Jurassic", "Cretaceous", "Paleogene", "Neogene", "Quaternary"]
Diet = Literal["Carnivore", "Herbivore", "Omnivore", "Piscivore", "Insectivore", "Filter Feeder"]
Habitat = Literal["Terrestrial", "Amphibious", "Aquatic", "Aerial", "Fossorial", "Arboreal"]

# Body for creating a record (no id, the database assigns it)
class PrehistoricCreatureCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    scientific_name: str = Field(min_length=1, max_length=150)
    period: Period
    diet: Diet
    family: str = Field(min_length=1, max_length=100)
    type: str = Field(min_length=1, max_length=50)
    defence: str = Field(min_length=1, max_length=255)
    location: str = Field(min_length=1, max_length=150)
    discovered: str = Field(min_length=1, max_length=150)
    life_span: str = Field(min_length=1, max_length=50)
    habitat: Habitat
    weight: str = Field(min_length=1, max_length=50)
    height: str = Field(min_length=1, max_length=50)
    extinction: str = Field(min_length=1, max_length=255)

# Body for a partial update (send only the fields to change)
class PrehistoricCreatureUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    scientific_name: Optional[str] = Field(default=None, min_length=1, max_length=150)
    period: Optional[Period] = None
    diet: Optional[Diet] = None
    family: Optional[str] = Field(default=None, min_length=1, max_length=100)
    type: Optional[str] = Field(default=None, min_length=1, max_length=50)
    defence: Optional[str] = Field(default=None, min_length=1, max_length=255)
    location: Optional[str] = Field(default=None, min_length=1, max_length=150)
    discovered: Optional[str] = Field(default=None, min_length=1, max_length=150)
    life_span: Optional[str] = Field(default=None, min_length=1, max_length=50)
    habitat: Optional[Habitat] = None
    weight: Optional[str] = Field(default=None, min_length=1, max_length=50)
    height: Optional[str] = Field(default=None, min_length=1, max_length=50)
    extinction: Optional[str] = Field(default=None, min_length=1, max_length=255)

# API KEY Authentication
def is_admin_key(x_api_key: Optional[str]):
    admin_key = os.environ.get("ADMIN_API_KEY")
    return bool(x_api_key and admin_key and secrets.compare_digest(x_api_key.encode(), admin_key.encode()))

# Read access: any website key or the admin key
def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key not in API_KEYS and not is_admin_key(x_api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key."
        )
    return True

# Write access (create, update, delete): admin key only
def verify_admin_key(x_api_key: Optional[str] = Header(default=None)):
    if is_admin_key(x_api_key):
        return True
    if x_api_key in API_KEYS:
        raise HTTPException(
            status_code=403,
            detail="Admin key required."
        )
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API key."
    )

#Error Handling 
@app.exception_handler(psycopg.OperationalError)
def database_unavailable(request, exc):
    return JSONResponse(
        status_code=503,
        content={"detail": "Database temporarily unavailable. Please try again later."}
    )

@app.exception_handler(psycopg.Error)
def database_error(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred."}
    )

@app.exception_handler(Exception)
def unexpected_error(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error."}
    )

#Health
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "DinoBase API",
        "version": API_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
@app.get("/health/db")
def database_health():
    try:
        from db import connect
        with connect():
            pass
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "detail": type(e).__name__}

# HOME
@app.get("/api/v1/")
def home():
    return {
        "message": "Welcome to the DinoBase API!",
        "endpoints": [
            "/api/v1/dinosaurs",
            "/api/v1/dinosaurs/{id}",
            "/api/v1/dinosaurs/search"
        ]
    }


# GET ALL DINOSAURS (optional ?period= ?diet= ?habitat= filters)
@app.get("/api/v1/dinosaurs", dependencies=[Depends(verify_api_key)])
def get_dinosaurs(
    period: Optional[Period] = None,
    diet: Optional[Diet] = None,
    habitat: Optional[Habitat] = None
):
    from db import connect
    with connect() as conn:
        dinosaurs = crud.list_creatures(conn, {"period": period, "diet": diet, "habitat": habitat})
    return {
        "count": len(dinosaurs),
        "dinosaurs": dinosaurs
    }


# SEARCH DINOSAURS — must stay declared before /dinosaurs/{id}
@app.get("/api/v1/dinosaurs/search", dependencies=[Depends(verify_api_key)])
def search_dinosaurs(q: str = Query(..., min_length=1)):
    from db import connect
    q = q.lower()
    with connect() as conn:
        results = crud.search_creatures(conn, q)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }


# GET ONE DINOSAUR
@app.get("/api/v1/dinosaurs/{dinosaur_id}", response_model=PrehistoricCreature, dependencies=[Depends(verify_api_key)])
def get_dinosaur(dinosaur_id: int):
    from db import connect
    with connect() as conn:
        dino = crud.get_creature(conn, dinosaur_id)

    if dino is None:
        raise HTTPException(
            status_code=404,
            detail="Dino not found."
        )
    return dino


# CREATE DINOSAUR (admin key required)
@app.post("/api/v1/dinosaurs", response_model=PrehistoricCreature, status_code=201, dependencies=[Depends(verify_admin_key)])
def create_dinosaur(new_dino: PrehistoricCreatureCreate):
    from db import connect
    try:
        with connect() as conn:
            dino = crud.create_creature(conn, new_dino.model_dump())
    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A dinosaur with that name or scientific name already exists."
        )
    return dino


# UPDATE DINOSAUR (admin key required, partial update)
@app.patch("/api/v1/dinosaurs/{dinosaur_id}", response_model=PrehistoricCreature, dependencies=[Depends(verify_admin_key)])
def update_dinosaur(dinosaur_id: int, changes: PrehistoricCreatureUpdate):
    from db import connect
    data = changes.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=422,
            detail="Provide at least one field to update."
        )
    if any(value is None for value in data.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null."
        )
    try:
        with connect() as conn:
            dino = crud.update_creature(conn, dinosaur_id, data)
    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A dinosaur with that name or scientific name already exists."
        )

    if dino is None:
        raise HTTPException(
            status_code=404,
            detail="Dino not found."
        )
    return dino


# DELETE DINOSAUR (admin key required)
@app.delete("/api/v1/dinosaurs/{dinosaur_id}", status_code=204, dependencies=[Depends(verify_admin_key)])
def delete_dinosaur(dinosaur_id: int):
    from db import connect
    with connect() as conn:
        deleted = crud.delete_creature(conn, dinosaur_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Dino not found."
        )
