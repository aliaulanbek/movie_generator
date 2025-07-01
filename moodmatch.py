import requests
import sqlite3

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

if __name__ == "__main__":
  main()