import requests
import sqlite3
import os 
from google import genai
from google.genai import types
import sqlalchemy as db
import pandas as pd


# AIzaSyDJbKD2e8V8MCyfLyM7xfJdSowXTeTwxMk
# 19278b5202f275d1776a68267c25054f

my_api_key = os.getenv('GENAI_KEY')
movie_api = os.getenv('MOVIE_REC')

DB_NAME = "movie_recommendations.db"
# todo: 
# figure out what columns to go in the table
# write the sql command for the dtabase 

def get_movies():
  tmdb_url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
  params = {
    "api_key" : movie_api
  }
  response = requests.get(tmdb_url, params)
  return response.json()['results']

def setup_database(movies):

  df = pd.DataFrame(movies)
  # print(df)

  df = df[['original_title', 'overview', 'release_date', 'vote_average']]
  engine = db.create_engine('sqlite:///movie_database.db')

  df.to_sql('movies', con=engine, if_exists='replace', index=False)

  with engine.connect() as connection:
    query_result = connection.execute(db.text("SELECT * FROM movies;")).fetchall()
    print(pd.DataFrame(query_result))

def ai_rec(mood, audience):
  genai.api_key = my_api_key

  # WRITE YOUR CODE HERE

  # Create an genAI client using the key from our environment variable
  client = genai.Client(
      api_key=my_api_key,
  )
  # Specify the model to use and the messages to send
  response = client.models.generate_content(
      model="gemini-2.5-flash",
      config=types.GenerateContentConfig(
        system_instruction= f"User is Felling this {mood} and they are watching a movie with {audience}."
      ),
      contents="What are the advantages of pair programming?",
  )

  print(response.text)

def main():
  # setup_database()

  print("Welcome to the Mood Match Movie Recommender!")
  mood = input("Enter your current mood: ").strip()
  audience = input("Who are you watching with? (e.g., alone, partner, friends, family): ").strip()
  popular_movies = get_movies()
  # print(popular_movies)
  setup_database(popular_movies)

  # ai_rec(mood, audience)


if __name__ == "__main__":
  main()