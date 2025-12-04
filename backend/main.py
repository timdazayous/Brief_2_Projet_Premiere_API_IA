# backend/main.py
from fastapi import FastAPI

# --- Configuration ---
app = FastAPI(title="API")

# --- Routes API ---
# http://www.google.com/fr route fr
# http://www.google.com/en route en 
# http://www.google.com/ route principale

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "API is running"}

@app.get("/citation")
def read_root():
    return {"auteur": "Cyril", "citation": "Caractéristique qui, pour tout ensemble, fini ou infini, permet de définir une notion équivalente au nombre d'éléments à travers la mise en place d'une bijection entre ensembles."}

@app.get("/fr")
def read_root():
    return {"Bonjour": "Monde", "status": "API est ok"}
