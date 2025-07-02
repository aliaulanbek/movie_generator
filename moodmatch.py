import requests
import sqlite3
import os 
from google import genai
from google.genai import types
import sqlalchemy as db
from sqlalchemy.types import VARCHAR, Float
import pandas as pd

my_api_key = os.getenv('GENAI_KEY')
movie_api = os.getenv('MOVIE_REC')

DB_NAME = "movie_recommendations.db"

def get_movies():
  max_pages = 5
  all_movies = []

  for i in range(1, 1 + max_pages):
    # tmdb_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={i}&sort_by=popularity.desc"
    tmdb_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={i}&sort_by=vote_average.desc&without_genres=99,10755&vote_count.gte=200"
    params = {
      "api_key" : movie_api
    }
    response = requests.get(tmdb_url, params)
    all_movies.extend(response.json()['results'])

  return all_movies

def setup_database(movies):

  df = pd.DataFrame(movies)
  df = df[['original_title', 'overview', 'vote_average']]
  engine = db.create_engine('sqlite:///movie_database.db')

  df.to_sql(
    'movies',
    con=engine,
    if_exists='replace',
    index=False,
    dtype={
        'original_title': VARCHAR(100),
        'overview': VARCHAR(1000),   chars
        'vote_average': db.Float
    }
  )

  with engine.connect() as connection:
    query_result = connection.execute(db.text("SELECT * FROM movies;")).fetchall()
    df_result = pd.DataFrame(query_result)
    pd.set_option('display.max_colwidth', None) 

    csv_text = df_result.to_csv(index=False)
    return csv_text

def ai_rec(mood, audience, db):
  genai.api_key = my_api_key

  # Create an genAI client using the key from our environment variable
  client = genai.Client(
    api_key=my_api_key,
  )

  prompt = f"User is feeling this {mood} and they are watching a movie with {audience}. Based on the following comma-separated list of movies (title, overview, rating): {db}, please print the title of the movie and its full overview in the following format (without asterisks): Title: Overview: " 
  # Specify the model to use and the messages to send
  response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
      system_instruction = prompt
    ),
    contents="Provide the top 3 movies that align with the user's mood and audience",
  )
  print(response.text)

def main():
  print("Welcome to the Mood Match Movie Recommender!")
  
  mood = input("Enter your current mood: ").strip()
  if len(mood) == 0:
    print("No mood entered. Quitting application")
    return
  audience = input("Who are you watching with? (e.g., alone, partner, friends, family): ").strip()
  if len(audience) == 0:
    print("No audience entered. Quitting application")
    return
  popular_movies = get_movies()
  db = setup_database(popular_movies)

  ai_rec(mood, audience, db)

if __name__ == "__main__":
  main()