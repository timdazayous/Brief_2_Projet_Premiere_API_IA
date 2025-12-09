from nltk.sentiment import SentimentIntensityAnalyzer
from pydantic import BaseModel
from pydantic import Field, BaseModel
from loguru import logger
import os
from fastapi import FastAPI
import uvicorn

# modèle pydantic
class QuoteIAnalyse(BaseModel):
    text : str = Field(min_length=1, description="donnez un texte pour la citation")

# initialisation de Vader
sia = SentimentIntensityAnalyzer()

app = FastAPI(title="API IA Sentiment")

#création du dossier logs si besoin
os.makedirs("logs", exist_ok=True)

logger.add("logs/sentiment_api.log", rotation="500 MB", level="INFO")


@app.post("/analyse_sentiment/")
def analyse_sentiment(quote: QuoteIAnalyse):
    """" Recoit un text (anglophone) et renvoie un score de sentiment par IA """
    logger.info(f"Analyse du texte: {quote.text}")
    try:
        sentiment = sia.polarity_scores(quote.text)
        logger.info(f"Resultats IA: {sentiment}")


        return {
            "neg": sentiment["neg"],
            "neu": sentiment["neu"],
            "pos": sentiment["pos"],
            "compound": sentiment["compound"]
        }
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse IA: {e}")


