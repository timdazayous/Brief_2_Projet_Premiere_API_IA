from nltk.sentiment import SentimentIntensityAnalyzer
from pydantic import BaseModel
from pydantic import Field, BaseModel
from loguru import logger
import os
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

load_dotenv()

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

# if __name__ == "__main__":
#     print("Hello")
#     url = os.getenv("API_BASE_URL", "127.0.0.1")
#     port_str = os.getenv("FAST_API_2_PORT", "8000")

#     try:
#         port = int(port_str)
#         print(port)
#     except ValueError:
#         print("ERREUR")
#         port = 8000

#     uvicorn.run(
#         app,               # on passe directement l'objet app, pas le chemin "API_IA.sentiment_api:app"
#         host=url,
#         port=port,
#         reload=False,
#     )

# if __name__ == "__main__":
#     import os
#     import uvicorn

#     print("Hello")
#     url = os.getenv("API_BASE_URL", "127.0.0.1")
#     port_str = os.getenv("FAST_API_2_PORT", "8000")

#     try:
#         port = int(port_str)
#         print(port)
#     except ValueError:
#         print("ERREUR")
#         port = 8000

#     uvicorn.run(
#         "API_IA.sentiment_api:app",  # <- correspond à ton arborescence
#         host=url,
#         port=port,
#         reload=True,
#     )

# if __name__ == "__main__":
#     # 1 - on récupère le port de l'API
#     try:
#         print("Hello")
#         port = os.getenv('FAST_API_2_PORT')
#         url = os.getenv('API_BASE_URL')
#         port = int(port)
#         print(port)
#     except ValueError:
#         print("ERREUR")
#         port = 8080

#     # 2 - On lance uvicorn
#     uvicorn.run(
#         "API_IA.sentiment_api:app", 
#         host = url,
#         port = port, 
#         reload = True
#     )

# if __name__ == "__main__": # uvicorn API_IA.sentiment_api:app --host 127.0.0.1 --port 9000 --reload

#     print("Hello")
#     url = os.getenv("API_BASE_URL", "127.0.0.1")
#     port_str = os.getenv("FAST_API_2_PORT", "9000")
#     try:
#         port = int(port_str)
#         print(port)
#     except ValueError:
#         print("ERREUR")
#         port = 9000
#     uvicorn.run(
#         "API_IA.sentiment_api:app",  # string
#         host=url,
#         port=port,
#         reload=True,
#     )

if __name__ == "__main__":
    import subprocess
    import sys

    # relance uvicorn comme tu le fais dans le terminal
    cmd = [
        sys.executable,               # python du venv
        "-m", "uvicorn",
        "API_IA.sentiment_api:app",
        "--host", "127.0.0.1",
        "--port", "9000",
        "--reload",
    ]
    subprocess.run(cmd)

    