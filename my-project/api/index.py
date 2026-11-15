import os
import secrets
import sys
from datetime import datetime, timezone
from typing import Literal, Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import psycopg
from fastapi import Depends, FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict, Field

import crud
from db import get_conn

API_VERSION = "1.0"


API_KEYS = {
    "nave-api-codex-110605": "nave-list-key",
    "nave-api-card-101707": "nave-rouge-key",
    "nave-api-crptic-112723": "nave-quiz-key",
}

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

Period = Literal["Cambrian", "Ordovician", "Silurian", "Devonian", "Carboniferous", "Permian", "Triassic", "Jurassic", "Cretaceous", "Paleogene", "Neogene", "Quaternary"]
Diet = Literal["Carnivore", "Herbivore", "Omnivore", "Piscivore", "Insectivore", "Filter Feeder"]
Habitat = Literal["Terrestrial", "Amphibious", "Aquatic", "Aerial", "Fossorial", "Arboreal"]


# DATA MODELS
class CreatureIn(BaseModel):
    """Body for creating a record. Every field is required."""
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


class PrehistoricCreature(CreatureIn):
    id: int


class CreatureUpdate(BaseModel):
    """Body for a partial update. Send only the fields you want to change."""
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


# AUTHENTICATION
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def _same(a: str, b: str) -> bool:
    return secrets.compare_digest(a.encode(), b.encode())


def get_key_role(x_api_key: Optional[str] = Depends(api_key_header)) -> str:
    admin_key = os.environ.get("ADMIN_API_KEY", "")
    if x_api_key and admin_key and _same(x_api_key, admin_key):
        return "admin"
    if x_api_key and any(_same(x_api_key, key) for key in API_KEYS):
        return "read"
    raise HTTPException(status_code=401, detail="Invalid or missing API key.")


def require_read(role: str = Depends(get_key_role)) -> str:
    return role


def require_admin(role: str = Depends(get_key_role)) -> str:
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin key required.")
    return role


# ERROR HANDLING 
@app.exception_handler(psycopg.OperationalError)
def database_unavailable(request, exc):
    return JSONResponse(status_code=503, content={"detail": "Database unavailable."})


@app.exception_handler(psycopg.Error)
def database_error(request, exc):
    return JSONResponse(status_code=500, content={"detail": "Database error."})


def run_write(conn, action):
    """Run a write, commit it, and turn database rule violations into clean errors."""
    try:
        result = action()
        conn.commit()
        return result
    except psycopg.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=409, detail="A dinosaur with that name or scientific name already exists.")
    except psycopg.errors.CheckViolation:
        conn.rollback()
        raise HTTPException(status_code=422, detail="Data breaks a database rule.")


# HEALTH
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "DinoBase API",
        "version": API_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


@app.get("/health/db")
def database_health(conn=Depends(get_conn)):
    conn.execute("SELECT 1")
    return {"status": "ok", "database": "connected"}


# HOME
@app.get("/api/v1/")
def home():
    return {
        "message": "Welcome to the DinoBase API!",
        "endpoints": [
            "/api/v1/dinosaurs",
            "/api/v1/dinosaurs/{id}",
            "/api/v1/dinosaurs/search",
        ],
    }


# LIST ALL
@app.get("/api/v1/dinosaurs", dependencies=[Depends(require_read)])
def get_dinosaurs(
    period: Optional[Period] = None,
    diet: Optional[Diet] = None,
    habitat: Optional[Habitat] = None,
    conn=Depends(get_conn),
):
    rows = crud.list_creatures(conn, {"period": period, "diet": diet, "habitat": habitat})
    return {"count": len(rows), "dinosaurs": rows}


# SEARCH ONE
@app.get("/api/v1/dinosaurs/search", dependencies=[Depends(require_read)])
def search_dinosaurs(q: str = Query(..., min_length=1), conn=Depends(get_conn)):
    rows = crud.search_creatures(conn, q)
    return {"query": q.lower(), "count": len(rows), "results": rows}


# READ: 
@app.get("/api/v1/dinosaurs/{dinosaur_id}", response_model=PrehistoricCreature, dependencies=[Depends(require_read)])
def get_dinosaur(dinosaur_id: int, conn=Depends(get_conn)):
    row = crud.get_creature(conn, dinosaur_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Dino not found.")
    return row


# CREATE
@app.post("/api/v1/dinosaurs", response_model=PrehistoricCreature, status_code=201, dependencies=[Depends(require_admin)])
def create_dinosaur(creature: CreatureIn, response: Response, conn=Depends(get_conn)):
    row = run_write(conn, lambda: crud.create_creature(conn, creature.model_dump()))
    response.headers["Location"] = f"/api/v1/dinosaurs/{row['id']}"
    return row


# UPDATE 
@app.patch("/api/v1/dinosaurs/{dinosaur_id}", response_model=PrehistoricCreature, dependencies=[Depends(require_admin)])
def update_dinosaur(dinosaur_id: int, changes: CreatureUpdate, conn=Depends(get_conn)):
    data = changes.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=422, detail="Provide at least one field to update.")
    if any(value is None for value in data.values()):
        raise HTTPException(status_code=422, detail="Fields cannot be null.")
    row = run_write(conn, lambda: crud.update_creature(conn, dinosaur_id, data))
    if row is None:
        raise HTTPException(status_code=404, detail="Dino not found.")
    return row


# DELETE
@app.delete("/api/v1/dinosaurs/{dinosaur_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_dinosaur(dinosaur_id: int, conn=Depends(get_conn)):
    deleted = run_write(conn, lambda: crud.delete_creature(conn, dinosaur_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Dino not found.")
    return Response(status_code=204)
