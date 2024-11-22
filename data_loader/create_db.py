import pandas as pd
from models import post
from models.database import SessionLocal, engine, BaseSQL

session = SessionLocal()

film_df = pd.read_json('films.json', orient='records')

cast_df = pd.read_csv('cast.csv')

def insert_films(session, film_df):
    for _, row in film_df.iterrows():
        film = post.Film(
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
            genres=row['Genres'], 
            time=row['Running Time (min)'],
            release_date=row['Release Date']
        )
        session.add(film)
    session.commit() 

def insert_casts(session, cast_df):
    for _, row in cast_df.iterrows():
        cast = post.Cast(
            id=row['id'],
            name=row['name'],
            role=row['role'],
            character_name=row['character_name'],
            image=row['image'],
            film_id=row['film_id']
        )
        session.add(cast)
    session.commit()


try:
    BaseSQL.metadata.create_all(bind=engine)
    insert_films(session, film_df)
    insert_casts(session, cast_df)
    print("Les données ont été insérées dans la base de données postgres.")
except Exception as e:
    print("Les données sont déjà dans la base de données postgres.")

session.close()