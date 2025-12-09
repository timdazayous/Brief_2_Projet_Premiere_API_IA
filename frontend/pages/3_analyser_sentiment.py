# API_IA\3_analyser_sentiment.py
import streamlit as st
import requests
from dotenv import load_dotenv
import os
from loguru import logger


load_dotenv()
API_ROOT_URL =  f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_2_PORT', '8080')}"
API_IA_URL =  API_ROOT_URL + "/analyse_sentiment/"

os.makedirs("logs", exist_ok=True)
logger.add("logs/sentiment_streamlit.log", rotation="500 MB", level="INFO")

st.title("Analyse de sentiment par IA")

text_to_analyse = st.text_area("Saisissez le texte à analyser ")

if st.button("Analyse IA"):
    if text_to_analyse:
        try:
            response = requests.post(API_IA_URL, json={"text": text_to_analyse})
            sentiment = response.json()

            st.write("Résultats de l'analyse IA Sentiment: ")
            st.write(f"Polarité négative : {sentiment['neg']} ")
            st.write(f"Polarité neutre   : {sentiment['neu']} ")
            st.write(f"Polarité positive : {sentiment['pos']} ")
            st.write(f"Polarité composée : {sentiment['compound']} ")

            logger.info(f"Affichage resultat: {sentiment}")
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API: {e}")
            logger.error(f"Erreur de connexion à l'API: {e}")
        except Exception as e:
            st.error(f"Une erreur est survenue: {e}")
            logger.error(f"Une erreur est survenue: {e}")
    else:
        st.warning("Veuillez entrez du texte pour le faire analyser")
        logger.info("Pas de texte saisi lors du clic de button")

