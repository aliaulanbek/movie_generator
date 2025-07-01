import requests
import sqlite3

DB_NAME = "movie_recommendations.db"

# day 4: database slides
def setup_database():
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()

# create table with data we want
  c.execute('sql comand')

  conn.commit()
  conn.close()

def main():
  setup_database()

  print("Welcome to the Mood Match Movie Recommender!")
  mood = input("Enter your current mood: ").strip()
  audience = input("Who are you watching with? (e.g., alone, partner, friends, family): ").strip()

if __name__ == "__main__":
  main()