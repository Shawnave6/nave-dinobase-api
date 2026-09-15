from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Literal

API_KEY = "nave-api-key-110605"
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

# DINOSAUR DATA
dinosaurs = [
    {
        "id": 1,
        "name": "Tyrannosaurus Rex",
        "scientific_name": "Tyrannosaurus rex",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Tyrannosauridae",
        "type": "Theropod",
        "defence": "Powerful jaws and strong bite",
        "location": "Western North America",
        "discovered": "Barnum Brown",
        "life_span": "28 to 33 years",
        "habitat": "Terrestrial",
        "weight": "5,000 to 9,000 kg",
        "height": "12 to 13 ft",
        "extinction": "Cretaceous-Paleogene extinction event"
    },
    {
        "id": 2,
        "name": "Triceratops",
        "scientific_name": "Triceratops horridus",
        "period": "Cretaceous",
        "diet": "Herbivore",
        "family": "Ceratopsidae",
        "type": "Ceratopsian",
        "defence": "Three horns and a large bony frill",
        "location": "Western North America",
        "discovered": "George Lyman Cannon",
        "life_span": "30 to 50 years",
        "habitat": "Terrestrial",
        "weight": "5,000 to 9,000 kg",
        "height": "9.5 to 12.5 ft",
        "extinction": "Cretaceous-Paleogene extinction event"
    },
    {
        "id": 3,
        "name": "Velociraptor",
        "scientific_name": "Velociraptor mongoliensis",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Dromaeosauridae",
        "type": "Theropod",
        "defence": "Sharp claws and agile movement",
        "location": "Gobi Desert and Northern China",
        "discovered": "Peter Kaisen",
        "life_span": "15 to 20 years",
        "habitat": "Terrestrial",
        "weight": "15 to 20 kg",
        "height": "1.6 to 2 ft",
        "extinction": "Cretaceous-Paleogene extinction event"
    },
    {
        "id": 4,
        "name": "Stegosaurus",
        "scientific_name": "Stegosaurus stenops",
        "period": "Jurassic",
        "diet": "Herbivore",
        "family": "Stegosauridae",
        "type": "Stegosaur",
        "defence": "Spiked tail and protective plates",
        "location": "Western North America",
        "discovered": "Arthur Lakes",
        "life_span": "25 to 30 years",
        "habitat": "Terrestrial",
        "weight": "5,300 to 7,000 kg",
        "height": "9 ft",
        "extinction": "Late Jurassic faunal turnover"
    },
    {
        "id": 5,
        "name": "Brachiosaurus",
        "scientific_name": "Brachiosaurus altithorax",
        "period": "Jurassic",
        "diet": "Herbivore",
        "family": "Brachiosauridae",
        "type": "Sauropod",
        "defence": "Large size and powerful tail",
        "location": "Western North America",
        "discovered": "Elmer S. Riggs",
        "life_span": "100 years",
        "habitat": "Terrestrial",
        "weight": "28,300 to 62,000 kg",
        "height": "41 to 49.2 ft",
        "extinction": "Climate change, oceanic anoxic events, and predation"
    },
    {
        "id": 6,
        "name": "Spinosaurus",
        "scientific_name": "Spinosaurus aegyptiacus",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Spinosauridae",
        "type": "Theropod",
        "defence": "Large size, powerful jaws, and strong claws",
        "location": "North Africa",
        "discovered": "Richard Markgraf",
        "life_span": "20 to 30 years",
        "habitat": "Amphibious",
        "weight": "6,400 to 7,400 kg",
        "height": "16 to 18 ft",
        "extinction": "Gradual environmental changes"
    },
    {
        "id": 7,
        "name": "Ankylosaurus",
        "scientific_name": "Ankylosaurus magniventris",
        "period": "Cretaceous",
        "diet": "Herbivore",
        "family": "Ankylosauridae",
        "type": "Ankylosaur",
        "defence": "Armored body and heavy tail club",
        "location": "Western North America",
        "discovered": "Barnum Brown",
        "life_span": "30 to 50 years",
        "habitat": "Terrestrial",
        "weight": "4,800 to 8,000 kg",
        "height": "5.6 ft",
        "extinction": "Cretaceous-Paleogene extinction event"
    },
    {
        "id": 8,
        "name": "Allosaurus",
        "scientific_name": "Allosaurus fragilis",
        "period": "Jurassic",
        "diet": "Carnivore",
        "family": "Allosauridae",
        "type": "Theropod",
        "defence": "Sharp teeth, claws, and powerful jaws",
        "location": "Western North America",
        "discovered": "Ferdinand Vandeveer Hayden",
        "life_span": "25 to 30 years",
        "habitat": "Terrestrial",
        "weight": "1,500 to 2,300 kg",
        "height": "9.5 to 16 ft",
        "extinction": "Environmental changes and faunal turnover"
    },
    {
        "id": 9,
        "name": "Diplodocus",
        "scientific_name": "Diplodocus carnegii",
        "period": "Jurassic",
        "diet": "Herbivore",
        "family": "Diplodocidae",
        "type": "Sauropod",
        "defence": "Long tail used as a possible whip-like weapon",
        "location": "Western United States",
        "discovered": "Samuel Wendell Williston",
        "life_span": "40 to 80 years",
        "habitat": "Terrestrial",
        "weight": "10,000 to 16,000 kg",
        "height": "11.5 to 16.4 ft",
        "extinction": "Gradual ecological transition"
    },
    {
        "id": 10,
        "name": "Parasaurolophus",
        "scientific_name": "Parasaurolophus walkeri",
        "period": "Cretaceous",
        "diet": "Herbivore",
        "family": "Hadrosauridae",
        "type": "Hadrosaur",
        "defence": "Large body and strong hind legs",
        "location": "Southwestern United States",
        "discovered": "William Parks",
        "life_span": "20 to 30 years",
        "habitat": "Terrestrial",
        "weight": "2,500 to 2,700 kg",
        "height": "9 ft",
        "extinction": "Uncertain"
    },
    {
        "id": 11,
        "name": "Pachycephalosaurus",
        "scientific_name": "Pachycephalosaurus wyomingensis",
        "period": "Cretaceous",
        "diet": "Omnivore",
        "family": "Pachycephalosauridae",
        "type": "Pachycephalosaur",
        "defence": "Thick, dome-shaped skull",
        "location": "Western North America",
        "discovered": "Ferdinand Vandeveer Hayden",
        "life_span": "20 to 30 years",
        "habitat": "Terrestrial",
        "weight": "370 to 500 kg",
        "height": "6 ft",
        "extinction": "Cretaceous-Paleogene extinction event"
    },
    {
        "id": 12,
        "name": "Carnotaurus",
        "scientific_name": "Carnotaurus sastrei",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Abelisauridae",
        "type": "Theropod",
        "defence": "Horns, powerful jaws, and muscular body",
        "location": "South America",
        "discovered": "Jose Bonaparte",
        "life_span": "20 to 30 years",
        "habitat": "Terrestrial",
        "weight": "1,350 to 2,100 kg",
        "height": "8 to 10 ft",
        "extinction": "Cretaceous-Paleogene extinction event"
    },
    {
        "id": 13,
        "name": "Iguanodon",
        "scientific_name": "Iguanodon bernissartensis",
        "period": "Cretaceous",
        "diet": "Herbivore",
        "family": "Iguanodontidae",
        "type": "Ornithopod",
        "defence": "Large thumb spike",
        "location": "Western Europe",
        "discovered": "Mary Ann Mantell",
        "life_span": "20 to 25 years",
        "habitat": "Terrestrial",
        "weight": "4,500 to 6,000 kg",
        "height": "9 to 13 ft",
        "extinction": "Environmental changes and faunal turnover"
    },
    {
        "id": 14,
        "name": "Compsognathus",
        "scientific_name": "Compsognathus longipes",
        "period": "Jurassic",
        "diet": "Carnivore",
        "family": "Compsognathidae",
        "type": "Theropod",
        "defence": "Small size and fast movement",
        "location": "Western Europe",
        "discovered": "Joseph Oberndorfer",
        "life_span": "10 to 15 years",
        "habitat": "Terrestrial",
        "weight": "0.8 to 3.5 kg",
        "height": "1 to 2 ft",
        "extinction": "Late Jurassic faunal turnover"
    },
    {
        "id": 15,
        "name": "Dilophosaurus",
        "scientific_name": "Dilophosaurus wetherilli",
        "period": "Jurassic",
        "diet": "Carnivore",
        "family": "Dilophosauridae",
        "type": "Theropod",
        "defence": "Powerful jaws and clawed hands",
        "location": "Western North America",
        "discovered": "Jesse Williams",
        "life_span": "20 years",
        "habitat": "Terrestrial",
        "weight": "400 to 500 kg",
        "height": "6 ft",
        "extinction": "Late Jurassic faunal turnover"
    },
    {
        "id": 16,
        "name": "Baryonyx",
        "scientific_name": "Baryonyx walkeri",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Spinosauridae",
        "type": "Theropod",
        "defence": "Large hooked claws and powerful jaws",
        "location": "Western Europe",
        "discovered": "William Walker",
        "life_span": "20 to 25 years",
        "habitat": "Amphibious",
        "weight": "1,200 to 2,000 kg",
        "height": "8 to 9 ft",
        "extinction": "Environmental changes"
    },
    {
        "id": 17,
        "name": "Giganotosaurus",
        "scientific_name": "Giganotosaurus carolinii",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Carcharodontosauridae",
        "type": "Theropod",
        "defence": "Large size and powerful jaws",
        "location": "South America",
        "discovered": "Ruben Carolini",
        "life_span": "40 to 60 years",
        "habitat": "Terrestrial",
        "weight": "6,500 to 8,000 kg",
        "height": "13 ft",
        "extinction": "Environmental changes and faunal turnover"
    },
    {
        "id": 18,
        "name": "Deinonychus",
        "scientific_name": "Deinonychus antirrhopus",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Dromaeosauridae",
        "type": "Theropod",
        "defence": "Large sickle-shaped toe claw",
        "location": "Western North America",
        "discovered": "John Ostrom",
        "life_span": "11 to 15 years",
        "habitat": "Terrestrial",
        "weight": "60 to 100 kg",
        "height": "2.5 to 3 ft",
        "extinction": "Environmental changes"
    },
    {
        "id": 19,
        "name": "Apatosaurus",
        "scientific_name": "Apatosaurus louisae",
        "period": "Jurassic",
        "diet": "Herbivore",
        "family": "Diplodocidae",
        "type": "Sauropod",
        "defence": "Large size and powerful tail",
        "location": "Western North America",
        "discovered": "Arthur Lakes",
        "life_span": "70 to 100 years",
        "habitat": "Terrestrial",
        "weight": "16,000 to 22,000 kg",
        "height": "15 ft",
        "extinction": "Late Jurassic faunal turnover"
    },
    {
        "id": 20,
        "name": "Styracosaurus",
        "scientific_name": "Styracosaurus albertensis",
        "period": "Cretaceous",
        "diet": "Herbivore",
        "family": "Ceratopsidae",
        "type": "Ceratopsian",
        "defence": "Long nose horn and multiple frill spikes",
        "location": "Western North America",
        "discovered": "Charles M. Sternberg",
        "life_span": "20 to 25 years",
        "habitat": "Terrestrial",
        "weight": "1,800 to 3,000 kg",
        "height": "5.5 to 6 ft",
        "extinction": "Cretaceous-Paleogene extinction event"
    }
]

# Validation
validated_dinosaurs = [PrehistoricCreature(**dino).model_dump() for dino in dinosaurs]
dinosaurs = validated_dinosaurs

# API KEY Authentication
def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key."
        )
    return True

#Health
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "DinoBase API",
        "version": API_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

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


# GET ALL DINOSAURS
@app.get("/api/v1/dinosaurs", dependencies=[Depends(verify_api_key)])
def get_dinosaurs():
    return {
        "count": len(dinosaurs),
        "dinosaurs": dinosaurs
    }


# SEARCH DINOSAURS — must stay declared before /dinosaurs/{id}
@app.get("/api/v1/dinosaurs/search", dependencies=[Depends(verify_api_key)])
def search_dinosaurs(q: str = Query(..., min_length=1)):
    q = q.lower()
    results = []
    for dino in dinosaurs:
        searchable_text = (
            f"{dino['name']} "
            f"{dino['scientific_name']} "
            f"{dino['period']} "
            f"{dino['diet']} "
            f"{dino['family']} "
            f"{dino['type']} "
            f"{dino['defence']}"
        ).lower()

        if q in searchable_text:
            results.append(dino)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }


# GET ONE DINOSAUR
@app.get("/api/v1/dinosaurs/{dinosaur_id}", response_model=PrehistoricCreature, dependencies=[Depends(verify_api_key)])
def get_dinosaur(dinosaur_id: int):
    for dino in dinosaurs:
        if dino["id"] == dinosaur_id:
            return dino

    raise HTTPException(
        status_code=404,
        detail="Dino not found."
    )
