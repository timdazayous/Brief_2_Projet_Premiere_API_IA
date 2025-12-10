# frontend/pages/2_rechercher.py
import streamlit as st
import requests 
import os 
import pandas as pd
from dotenv import load_dotenv 

load_dotenv()

API_ROOT_URL =  f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '9090')}"
API_IA_URL = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_2_PORT', '8080')}/analyse_sentiment"

st.title("Lire une citation")

mode = st.radio("Choisissez le mode de recherche:",
         ("Aléatoire", "Par ID "))

if mode == "Aléatoire":
    st.subheader("Citation Aléatoire")
    # afficher une citation aléatoire
    API_URL =  API_ROOT_URL + "/read/random/"
    if st.button("obetnir une citation aléatoire:"):
        try : 
            response = requests.get(API_URL)

            if response.status_code == 200:
                result = response.json()

                if result:
                    st.success(f"Citation avec ID {result.get('id', 'N/A')}")
                    st.info(result.get('text', 'text non trouvé'))
                    st.balloons()


                    # bouton pour l'analyse IA
                    if st.button("Analyser Sentment IA pour la citation"):
                        try:
                            response_ia = requests.post(API_IA_URL, json={"text": result.get("text", "")})
                            if response_ia.status_code == 200:
                                sentiment = response_ia.json()
                                st.write("Résultats de l'analyse IA :")
                                st.write(f"Polarité négative : {sentiment['neg']}")
                                st.write(f"Polarité neutre   : {sentiment['neu']}")
                                st.write(f"Polarité positive : {sentiment['pos']}")
                                st.write(f"Polarité composée : {sentiment['compound']}")
                            else:
                                st.error(f"Erreur de l'API IA: {response_ia.status_code} - {response_ia.text}")    
                        except requests.exceptions.RequestException as e:
                            st.error(f"Erreur de connexion à l'API IA: {e}")
                else:
                    st.warning("Aucune citation disponible dans la DB")
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")


        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
            st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")

else:
    # afficher une citation par ID
    st.subheader("Citation par ID")
    API_URL =  API_ROOT_URL + "/read/"
    # selectionne l'ID
    # un formulaire
    with st.form("search_by_id"):
        quote_id = st.number_input("Entrez l'ID de la citation:", 
                                   min_value=1, step=1)
        submitted = st.form_submit_button("Rechercher")
    # connaitre toutes les id
    # selectionne l'id
    if submitted:
        # appel la route /read/id
        try : 
            response = requests.get( API_URL + str(quote_id) )
        # le reste est pareil
            if response.status_code == 200:
                result = response.json()

                if result:
                    st.success(f"Citation avec ID {quote_id}")
                    st.info(result.get('text', 'text non trouvé'))
                    st.balloons()

                    # bouton analyse de la citation par sentiment IA
                    if st.button("Analyser le sentiment de cette citation (ID)"):
                        try:
                            resp_ia = requests.post(
                                API_IA_URL,
                                json={"text": result.get("text", "")}
                            )
                            if resp_ia.status_code == 200:
                                sentiment = resp_ia.json()
                                st.write("Résultats de l'analyse IA :")
                                st.write(f"Polarité négative : {sentiment['neg']}")
                                st.write(f"Polarité neutre   : {sentiment['neu']}")
                                st.write(f"Polarité positive : {sentiment['pos']}")
                                st.write(f"Polarité composée : {sentiment['compound']}")
                            else:
                                st.error(f"Erreur de l'API IA: {resp_ia.status_code} - {resp_ia.text}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Erreur de connexion à l'API IA: {e}")
                
                else:
                    st.warning(f"La citation {quote_id} n'est pas disponible dans la DB")
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")


        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
            st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")