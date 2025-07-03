import requests
import sqlite3
import os 
from google import genai
from google.genai import types
import sqlalchemy as db
from sqlalchemy.types import VARCHAR, Float
import pandas as pd
from sqlalchemy import inspect

my_api_key = os.getenv('GENAI_KEY')
movie_api = os.getenv('MOVIE_REC')

DB_FILE_NAME = "movie_recommendations.db"

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
    response.raise_for_status()
    all_movies.extend(response.json()['results'])

  return all_movies

def get_db_engine():
    return db.create_engine(f'sqlite:///{DB_FILE_NAME}')

def setup_database(movies):

  engine = get_db_engine()
  df = pd.DataFrame(movies)
  df = df[['original_title', 'overview', 'vote_average']]
  table_name = 'movies'

  inspector = inspect(engine)
  if table_name in inspector.get_table_names():
    with engine.connect() as connection:
      existing_titles = pd.read_sql(f"SELECT original_title FROM {table_name}", connection)['original_title'].tolist()

    movies_to_add_df = df[~df['original_title'].isin(existing_titles)]

    if not movies_to_add_df.empty:
      movies_to_add_df.to_sql(
        table_name,
        con=engine,
        if_exists='append', # Append new data
        index=False,
        dtype={
          'original_title': VARCHAR(100),
          'overview': VARCHAR(1000),
          'vote_average': db.Float
        }
      )
  else:
    df.to_sql(
      table_name,
      con=engine,
      if_exists='replace', # Use 'replace' only for the very first creation if table doesn't exist
      index=False,
      dtype={
          'original_title': VARCHAR(100),
          'overview': VARCHAR(1000),
          'vote_average': db.Float
      }
    )

  with engine.connect() as connection:
    query_result = connection.execute(db.text(f"SELECT * FROM {table_name};")).fetchall()
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

  prompt =  "You are a movie recommendation AI. You will receive a user's mood, their audience, "
  "and a list of movies (title, overview, rating). Your task is to recommend movies "
  "from the provided list that align with the user's preferences."

  query = f"The user is feeling '{mood}' and they are watching a movie with '{audience}'.\n"
  "Based on the following comma-separated list of movies (title, overview, rating):\n"
  f"{db}\n\n" # Pass the CSV content here
  "Please provide the top 3 movie recommendations. For each recommendation, "
  "print the movie title and its full overview in the following format (without asterisks or extra formatting beyond what's specified): \n"
  "Title: [Movie Title]\n"
  "Overview: [Movie Overview]\n\n"

  response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
      system_instruction = prompt
    ),
    contents= query
  )
  print(response.text)

def main():
  print("Welcome to MoodFlix!")
  
  mood = input("Enter your current mood: ").strip()
  if len(mood) == 0:
    print("No mood entered. Quitting application")
    return
  audience = input("Who are you watching with? (e.g., alone, partner, friends, family): ").strip()
  if len(audience) == 0:
    print("No audience entered. Quitting application")
    return
  print("\n")
  popular_movies = get_movies()
  db = setup_database(popular_movies)

  ai_rec(mood, audience, db)

if __name__ == "__main__":
  main()