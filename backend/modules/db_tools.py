# backend/modules/df_tools.py
from loguru import logger 
import pandas as pd
import os 
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, session


DB_FILE_PATH = os.path.join("backend","data", "quotes_db.sql")
engine = create_engine(f"sqlite:///{DB_FILE_PATH}", echo=False)
session_locale = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)

TABLE_NAME = "quotes"
#CSV_FILE_PATH = os.path.join("backend","data", "quotes_db.csv")

def get_session():
    return session_locale() # permet de créer une session quand on en a besoin

def write_db(df: pd.DataFrame):
    #df.to_csv(CSV_FILE_PATH, index=True, index_label='id')
    #print("write_df\n", df)
    df.to_sql(
        TABLE_NAME,
        con=engine,
        if_exists='replace', # supprime et remplace la db si deja existante avec la nouvelle db modifiée
        index=True,
        index_label='id'
    )

def read_db()->pd.DataFrame:
    # df = pd.read_csv(CSV_FILE_PATH, index_col='id')

    # if df.isnull().any().any():
    #     # raise ValueError("Le CSV contient des valeurs nulles")
    #     df_clean = df.dropna()
    # for r, c in df.iterrows():
    #     print(c.text.isempty)
    with get_session() as session:
        quotes = session.query(Quote).all() # la liste des objets Quote

    # on veut transformer en dataframe comme dans df_tools 
    # on créer une liste de dictionnaires id:text representant chaques row de quotes
    data = [{"id": q.id, "text": q.text} for q in quotes]
    
    if not data:
        # cas index vide pris en compte
        return pd.DataFrame(columns=["text"])
    
    df = pd.DataFrame(data).set_index("id")

    df = df.astype("object")

    # nettoayge NAN comme dans 
    if df.isna().any().any():  # <-- MODIF 2 : check global des NaN [web:1]
        logger.info("NaN trouvés dans le DataFrame, remplacement par 'NULL_REPLACEMENT_VALUE'")
        df = df.fillna("NULL_REPLACEMENT_VALUE")  # <-- MODIF 3 : remplacement propre des NaN [web:1]

    return df

    # for index, row in df.iterrows() : 
    #     for col in df.columns:
    #         if pd.isna(row[col]):
    #             logger.info(f"NaN trouvé à la ligne {index}, colonne '{col}' remplacé par la valeur 'NULL'")
    #             df.loc[index, col] = "NULL_REPLACEMENT_VALUE"
    
    # # print("DATA =", data)
    # # print("COLUMNS =", df.columns)

    return df

def initialize_db():
    # if os.path.exists(CSV_FILE_PATH):
    #     logger.info("La base de données existe")
    # else:
    #     logger.info(f"impossible de trouver le fichier {CSV_FILE_PATH}")
    #     df = pd.DataFrame(columns=['id', 'text'])
    #     df = df.set_index('id')
    #     write_db(df)
    #     logger.info(f"le fichier {CSV_FILE_PATH} a été créé")

    if os.path.exists(DB_FILE_PATH):
        logger.info("La base de données existe déjà")
    else:
        Base.metadata.create_all(bind=engine) 
        logger.info(f"Base de données SQL {DB_FILE_PATH} créée")

