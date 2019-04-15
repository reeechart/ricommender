import pandas as pd

from django_pandas.io import read_frame

class MusicRecommendationCalculator():
    def __init__(self, user, location, weather):
        self.user = user
        self.location = location
        self.weather = weather
        self.history_data = []

    def _do_clustering(self):
        print(self.history_data)
        self.history_data.to_csv('concantenated_music_history.csv', index=False)

    def get_top_thirty_recommendation(self, history_data):
        self.history_data = read_frame(history_data)
        self._do_clustering()
