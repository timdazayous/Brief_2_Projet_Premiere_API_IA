# from fastapi.testclient import TestClient

# from backend.main import app
# from API_IA.sentiment_api import app

# from loguru import logger

# logger.remove()
# logger.add("tests/logs/log_test.log")

# client = TestClient(app)

# def test_root():
#     response = client.get("/")
#     test = response.status_code == 200
#     if test:
#         logger.info("La requete GET sur la route '/' a reussie")
#     else:
#         logger.error("La requete GET sur la route '/' a echouée ")
#     assert test