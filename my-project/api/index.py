from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DinoBase API",
    description="A beginner-friendly REST API containing information about dinosaurs.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DINOSAUR DATA
dinosaurs = [
    {
        "name": "Tyrannosaurus Rex",
        "scientific_name": "Tyrannosaurus rex",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Tyrannosauridae",
        "type": "Theropod",
        "defence": "Powerful jaws and strong bite"
    },
    {
        "name": "Triceratops",
        "scientific_name": "Triceratops horridus",
        "period": "Cretaceous",
        "diet": "Herbivore",
        "family": "Ceratopsidae",
        "type": "Ceratopsian",
        "defence": "Three horns and a large bony frill"
    },
    {
        "name": "Velociraptor",
        "scientific_name": "Velociraptor mongoliensis",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Dromaeosauridae",
        "type": "Theropod",
        "defence": "Sharp claws and agile movement"
    },
    {
        "name": "Stegosaurus",
        "scientific_name": "Stegosaurus stenops",
        "period": "Jurassic",
        "diet": "Herbivore",
        "family": "Stegosauridae",
        "type": "Stegosaur",
        "defence": "Spiked tail and protective plates"
    },
    {
        "name": "Brachiosaurus",
        "scientific_name": "Brachiosaurus altithorax",
        "period": "Jurassic",
        "diet": "Herbivore",
        "family": "Brachiosauridae",
        "type": "Sauropod",
        "defence": "Large size and powerful tail"
    },
    {
        "name": "Spinosaurus",
        "scientific_name": "Spinosaurus aegyptiacus",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Spinosauridae",
        "type": "Theropod",
        "defence": "Large size, powerful jaws, and strong claws"
    },
    {
        "name": "Ankylosaurus",
        "scientific_name": "Ankylosaurus magniventris",
        "period": "Cretaceous",
        "diet": "Herbivore",
        "family": "Ankylosauridae",
        "type": "Ankylosaur",
        "defence": "Armored body and heavy tail club"
    },
    {
        "name": "Allosaurus",
        "scientific_name": "Allosaurus fragilis",
        "period": "Jurassic",
        "diet": "Carnivore",
        "family": "Allosauridae",
        "type": "Theropod",
        "defence": "Sharp teeth, claws, and powerful jaws"
    },
    {
        "name": "Diplodocus",
        "scientific_name": "Diplodocus carnegii",
        "period": "Jurassic",
        "diet": "Herbivore",
        "family": "Diplodocidae",
        "type": "Sauropod",
        "defence": "Long tail used as a possible whip-like weapon"
    },
    {
        "name": "Parasaurolophus",
        "scientific_name": "Parasaurolophus walkeri",
        "period": "Cretaceous",
        "diet": "Herbivore",
        "family": "Hadrosauridae",
        "type": "Hadrosaur",
        "defence": "Large body and strong hind legs"
    },
    {
        "name": "Pachycephalosaurus",
        "scientific_name": "Pachycephalosaurus wyomingensis",
        "period": "Cretaceous",
        "diet": "Omnivore",
        "family": "Pachycephalosauridae",
        "type": "Pachycephalosaur",
        "defence": "Thick, dome-shaped skull"
    },
    {
        "name": "Carnotaurus",
        "scientific_name": "Carnotaurus sastrei",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Abelisauridae",
        "type": "Theropod",
        "defence": "Horns, powerful jaws, and muscular body"
    },
    {
        "name": "Iguanodon",
        "scientific_name": "Iguanodon bernissartensis",
        "period": "Cretaceous",
        "diet": "Herbivore",
        "family": "Iguanodontidae",
        "type": "Ornithopod",
        "defence": "Large thumb spike"
    },
    {
        "name": "Compsognathus",
        "scientific_name": "Compsognathus longipes",
        "period": "Jurassic",
        "diet": "Carnivore",
        "family": "Compsognathidae",
        "type": "Theropod",
        "defence": "Small size and fast movement"
    },
    {
        "name": "Dilophosaurus",
        "scientific_name": "Dilophosaurus wetherilli",
        "period": "Jurassic",
        "diet": "Carnivore",
        "family": "Dilophosauridae",
        "type": "Theropod",
        "defence": "Powerful jaws and clawed hands"
    },
    {
        "name": "Baryonyx",
        "scientific_name": "Baryonyx walkeri",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Spinosauridae",
        "type": "Theropod",
        "defence": "Large hooked claws and powerful jaws"
    },
    {
        "name": "Giganotosaurus",
        "scientific_name": "Giganotosaurus carolinii",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Carcharodontosauridae",
        "type": "Theropod",
        "defence": "Large size and powerful jaws"
    },
    {
        "name": "Deinonychus",
        "scientific_name": "Deinonychus antirrhopus",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Dromaeosauridae",
        "type": "Theropod",
        "defence": "Large sickle-shaped toe claw"
    },
    {
        "name": "Apatosaurus",
        "scientific_name": "Apatosaurus louisae",
        "period": "Jurassic",
        "diet": "Herbivore",
        "family": "Diplodocidae",
        "type": "Sauropod",
        "defence": "Large size and powerful tail"
    },
    {
        "name": "Styracosaurus",
        "scientific_name": "Styracosaurus albertensis",
        "period": "Cretaceous",
        "diet": "Herbivore",
        "family": "Ceratopsidae",
        "type": "Ceratopsian",
        "defence": "Long nose horn and multiple frill spikes"
    }
]

# HOME
@app.get("/")
def home():

    return {
        "message": "Welcome to the DinoBase API!",
        "endpoints": [
            "/dinosaurs",
            "/dinosaurs/{id}",
            "/dinosaurs/search"
        ]
    }


# GET ALL DINOSAURS
@app.get("/dinosaurs")
def get_dinosaurs():

    return {
        "count": len(dinosaurs),
        "dinosaurs": dinosaurs
    }


# GET ONE DINOSAUR
@app.get("/dinosaurs/{dinosaur_id}")
def get_dinosaur(dinosaur_id: int):
    for dino in dinosaurs:
        if dino["id"] == dinosaur_id:
            return dino

    raise HTTPException(
        status_code=404,
        detail="Dino not found."
    )

# SEARCH DINOSAURS
@app.get("/dinosaurs/search")
def search_dinosaurs( q: str = Query(..., min_length=1)):
    q = q.lower()
    results = []
    for dino in dinosaurs:
        searchable_text = (
            f"{dino['name']} "
            f"{dino['scientific_name']} "
            f"{dino['period']} "
            f"{dino['diet']} "
            f"{dino['family']} "
            f"{dino['type']}"
            f"{dino['defence']}"
        ).lower()

        if q in searchable_text:
            results.append(dino)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }
