import unittest
import moodmatch

class TestMovie(unittest.TestCase):

    def test_get_movie(self):
        movies = moodmatch.get_movies()
        self.assertIsInstance(movies, list)
        self.assertGreater(len(movies),0)

    
    def test_database_output(self):
        sample_movies = [
            {
                "original_title": "Home Alone",
                "overview": "An 8 year old troublemaker must protect his house from a pair of burglars when he's accidentally left home alone by his family during Christmas vacation",
                "vote_average": 7.7
            }
        ]
        csv_output = moodmatch.setup_database(sample_movies).strip()
        sample_result =  ("original_title,overview,vote_average\n"
                         "Home Alone,An 8 year old troublemaker must protect his house from a pair of burglars when he's accidentally left home alone by his family during Christmas vacation,7.7")
        self.assertEqual(csv_output, sample_result)

    def test_ai_rec_runs(self):
        mood = "Christmas spirit"
        audience = "Family"
        db = "Home Alone,An 8 year old troublemaker must protect his house from a pair of burglars when he's accidentally left home alone by his family during Christmas vacation,7.7"

        moodmatch.ai_rec(mood, audience, db)

        self.assertTrue(True)
