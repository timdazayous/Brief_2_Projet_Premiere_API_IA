#### Installation des bibliothèques
`pip install fastapi uvicorn`

Un mini programme complet:
* **frontend** (streamlit)
  * **pages**
* **backend**:
  * **modules** (contenir nos propres modules)
  * **data** (nos csv)

#### Architecture
```
mon_projet/
├── backend
│   ├── modules
│   │   └── 
│   ├── data
│   │   └── 
│   └── main.py
├── frontend
│   ├── app.py
│   └── pages
│       ├──
│       └── 
├── README.md
├── .venv
└── .gitignore
```

#### Commandes pour lancer le serveur uvicorn

`uvicorn chemin.nom:app --reload --log-level debug`

#### Commandes pour le terminale pour faire un GET
- `Powershell` : `Invoke-WebRequest -Method GET "http://127.0.0.1:8000/citation"`

- `MAC Linux` : `CURL -X GET "http://127.0.0.1:8000/citation"`