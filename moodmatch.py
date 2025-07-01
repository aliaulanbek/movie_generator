import requests
import sqlite3
import os 
from google import genai
from google.genai import types

# AIzaSyDJbKD2e8V8MCyfLyM7xfJdSowXTeTwxMk
# 19278b5202f275d1776a68267c25054f

DB_NAME = "movie_recommendations.db"
# todo: 
# figure out what columns to go in the table
# write the sql command for the dtabase 

# day 4: database slides
def setup_database():
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()

# create table with data we want
  c.execute('sql command')

  conn.commit()
  conn.close()

def main():
  setup_database()

  print("Welcome to the Mood Match Movie Recommender!")
  mood = input("Enter your current mood: ").strip()
  audience = input("Who are you watching with? (e.g., alone, partner, friends, family): ").strip()

  ai_rec(mood, audience)

def ai_rec(mood, audience):
  # Set environment variables
  my_api_key = os.getenv('GENAI_KEY')

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

if __name__ == "__main__":
  main()