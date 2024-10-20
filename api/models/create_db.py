import pandas as pd
from sqlalchemy.orm import Session
from post import Film, Cast
from database import SessionLocal
  # Importer votre session SQLAlchemy

# Créer une session de base de données
session = SessionLocal()

# Charger les films à partir du fichier CSV
film_df = pd.read_csv('film.csv')

# Charger les castings à partir du fichier CSV
cast_df = pd.read_csv('cast.csv')

# Fonction pour remplir la table des films
def insert_films(session, film_df):
    for _, row in film_df.iterrows():
        film = Film(
            id=row['id'],
            rank=row['rank'],
            title=row['title'],
            gross=row['gross'],
            year=row['year'],
            summary=row['summary'],
            image=row['image'],
            distributor=row['Domestic distributor'],
            budget=row['Budget'],
            MPAA=row['MPAA'],
            genres=row['Genres'].split(','),  # Convertion de chaîne en liste
            time=row['Running Time (min)'],
            release_date=row['Release Date']
        )
        session.add(film)
    session.commit()  # Valider l'insertion des films

# Fonction pour remplir la table des castings
def insert_casts(session, cast_df):
    for _, row in cast_df.iterrows():
        cast = Cast(
            id=row['id'],
            name=row['name'],
            role=row['role'],
            character_name=row['character_name'],
            image=row['image'],
            film_id=row['film_id']
        )
        session.add(cast)
    session.commit()  # Valider l'insertion des castings

# Insérer les données dans la base de données
insert_films(session, film_df)
insert_casts(session, cast_df)

# Fermer la session après insertion
session.close()
