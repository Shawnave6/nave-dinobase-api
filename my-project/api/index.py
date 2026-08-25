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
        "id": 1,
        "name": "Tyrannosaurus Rex",
        "scientific_name": "Tyrannosaurus rex",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Tyrannosauridae",
        "type": "Theropod",
        "defence": "Powerful jaws and strong bite"
        "location": "Western North America"
        "discovered": "Barnum Brown"
        "life_span": "28 to 30 years"
        "bite_force": "431,000 psi"
        "weight": "6,000 to 9,000 kg"
        "height": "12 to 13 ft"
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
        "defence": "Three horns and a large bony frill"
        "location": "Western North America"
        "discovered": "George Lyman Cannon"
        "life_span": "30 to 50 years"
        "bite_force": "8,000-10,000 psi"
        "weight": "6,000 to 12,000 kg"
        "height": "10.8 to 12.5 ft"
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
        "defence": "Sharp claws and agile movement"
        "location": "Gobi Desert and Northern China"
        "discovered": "Peter Kaisen"
        "life_span": "15 to 20 years"
        "bite_force": "1,000 psi"
        "weight": "14 to 20 kg"
        "height": "4.9 to 6.8 ft"
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
        "defence": "Spiked tail and protective plates"
        "location": "Western North America"
        "discovered": "Othniel Charles Marsh"
        "life_span": "25 to 30 years"
        "bite_force": "300 psi"
        "weight": "2,700 to 4,000 kg"
        "height": "21 to 30 ft"
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
        "defence": "Large size and powerful tail"
        "location": "Western North America"
        "discovered": "Elmer S. Riggs"
        "life_span": "100 years"
        "bite_force": "12,800 psi"
        "weight": "28,300 to 62,000 kilograms"
        "height": "41 to 49.2 ft"
        "extinction": "Climate change, Oceanic anoxic events, and Predation"
    },
    {
        "id": 6,
        "name": "Spinosaurus",
        "scientific_name": "Spinosaurus aegyptiacus",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Spinosauridae",
        "type": "Theropod",
        "defence": "Large size, powerful jaws, and strong claws"
        "location": "North Africa"
        "discovered": "Ernst Stromer"
        "life_span": "20 to 30 years"
        "bite_force": "4,000 to 4,200 psi"
        "weight": "6,400 to 7,400 kg"
        "height": "16 to 18 ft"
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
        "defence": "Armored body and heavy tail club"
        "location": "Western North America"
        "discovered": "Barnum Brown"
        "life_span": "30 to 50 years"
        "bite_force": "600 to 700 psi"
        "weight": "4,800 to 8,000 kg"
        "height": "5.6 to 6.6 ft"
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
        "defence": "Sharp teeth, claws, and powerful jaws"
        "location": "Western North America"
        "discovered": "Othniel Charles Marsh"
        "life_span": "28 years"
        "bite_force": "2,100 psi"
        "weight": "1,500 to 2,500 kilograms"
        "height": "8 to 16 ft"
        "extinction": "Environmental changes and Faunal turnover"
    },
    {
        "id": 9,
        "name": "Diplodocus",
        "scientific_name": "Diplodocus carnegii",
        "period": "Jurassic",
        "diet": "Herbivore",
        "family": "Diplodocidae",
        "type": "Sauropod",
        "defence": "Long tail used as a possible whip-like weapon"
        "location": "Western United States"
        "discovered": "Samuel Wendell Williston"
        "life_span": "40 to 80 years"
        "bite_force": "250–300 psi"
        "weight": "10,000 to 16,000 kg"
        "height": "11.5 to 16.4 ft"
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
        "defence": "Large body and strong hind legs"
        "location": "Southwestern United States"
        "discovered": "William Parks"
        "life_span": "20 to 30 years"
        "bite_force": "1,800 psi"
        "weight": "2,000 to 5,000 kg"
        "height": "14.4 to 18.4 ft"
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
        "defence": "Thick, dome-shaped skull"
        "location": "Western North America"
        "discovered": "Ferdinand Vandeveer Hayden"
        "life_span": "20 to 30 years"
        "bite_force": "250 to 300 psi"
        "weight": "370 to 500 kg"
        "height": "6 ft"
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
        "defence": "Horns, powerful jaws, and muscular body"
        "location": "South America"
        "discovered": "José Bonaparte"
        "life_span": "20 to 30 years"
        "bite_force": "3,000 to 4,000 psi"
        "weight":
        "height":
        "extinction":
    },
    {
        "id": 13,
        "name": "Iguanodon",
        "scientific_name": "Iguanodon bernissartensis",
        "period": "Cretaceous",
        "diet": "Herbivore",
        "family": "Iguanodontidae",
        "type": "Ornithopod",
        "defence": "Large thumb spike"
        "location":
        "discovered":
        "life_span":
        "bite_force":
        "weight":
        "height":
        "extinction":
    },
    {
        "id": 14,
        "name": "Compsognathus",
        "scientific_name": "Compsognathus longipes",
        "period": "Jurassic",
        "diet": "Carnivore",
        "family": "Compsognathidae",
        "type": "Theropod",
        "defence": "Small size and fast movement"
        "location":
        "discovered":
        "life_span":
        "bite_force":
        "weight":
        "height":
        "extinction":
    },
    {
        "id": 15,
        "name": "Dilophosaurus",
        "scientific_name": "Dilophosaurus wetherilli",
        "period": "Jurassic",
        "diet": "Carnivore",
        "family": "Dilophosauridae",
        "type": "Theropod",
        "defence": "Powerful jaws and clawed hands"
        "location":
        "discovered":
        "life_span":
        "bite_force":
        "weight":
        "height":
        "extinction":
    },
    {
        "id": 16,
        "name": "Baryonyx",
        "scientific_name": "Baryonyx walkeri",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Spinosauridae",
        "type": "Theropod",
        "defence": "Large hooked claws and powerful jaws"
        "location":
        "discovered":
        "life_span":
        "bite_force":
        "weight":
        "height":
        "extinction":
    },
    {
        "id": 17,
        "name": "Giganotosaurus",
        "scientific_name": "Giganotosaurus carolinii",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Carcharodontosauridae",
        "type": "Theropod",
        "defence": "Large size and powerful jaws"
        "location":
        "discovered":
        "life_span":
        "bite_force":
        "weight":
        "height":
        "extinction":
    },
    {
        "id": 18,
        "name": "Deinonychus",
        "scientific_name": "Deinonychus antirrhopus",
        "period": "Cretaceous",
        "diet": "Carnivore",
        "family": "Dromaeosauridae",
        "type": "Theropod",
        "defence": "Large sickle-shaped toe claw"
        "location":
        "discovered":
        "life_span":
        "bite_force":
        "weight":
        "height":
        "extinction":
    },
    {
        "id": 19,
        "name": "Apatosaurus",
        "scientific_name": "Apatosaurus louisae",
        "period": "Jurassic",
        "diet": "Herbivore",
        "family": "Diplodocidae",
        "type": "Sauropod",
        "defence": "Large size and powerful tail"
        "location":
        "discovered":
        "life_span":
        "bite_force":
        "weight":
        "height":
        "extinction":
    },
    {
        "id": 20,
        "name": "Styracosaurus",
        "scientific_name": "Styracosaurus albertensis",
        "period": "Cretaceous",
        "diet": "Herbivore",
        "family": "Ceratopsidae",
        "type": "Ceratopsian",
        "defence": "Long nose horn and multiple frill spikes"
        "location":
        "discovered":
        "life_span":
        "bite_force":
        "weight":
        "height":
        "extinction":
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

