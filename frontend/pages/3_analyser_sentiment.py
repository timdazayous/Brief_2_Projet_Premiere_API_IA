import streamlit as st
import requests
import dotenv
import os
from loguru import logger


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
