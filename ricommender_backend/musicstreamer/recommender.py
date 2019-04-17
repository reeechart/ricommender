import numpy as np
import pandas as pd

from django_pandas.io import read_frame

from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

class MusicRecommendationCalculator():
    def __init__(self, user, location, weather):
        self.user = user
        self.location = location
        self.weather = weather
        self.history_data = []
        self.normalized_history_data = []
        self.music_data = []
        self.n_cluster=15
        self.cov_type='full'

    def _normalize_history_data_context(self):
        one_hot_encoded_location = pd.get_dummies(self.normalized_history_data['location'], prefix='location')
        one_hot_encoded_weather = pd.get_dummies(self.normalized_history_data['weather'], prefix='weather')
        self.normalized_history_data = pd.concat([one_hot_encoded_weather, self.normalized_history_data], axis=1)
        self.normalized_history_data = pd.concat([one_hot_encoded_location, self.normalized_history_data], axis=1)

    def _normalize_history_data_username(self):
        one_hot_encoded_username = pd.get_dummies(self.normalized_history_data['user'], prefix='user')
        self.normalized_history_data = pd.concat([one_hot_encoded_username, self.normalized_history_data], axis=1)

    def _drop_string_nominal_attributes(self):
        self.normalized_history_data = self.normalized_history_data.drop(['user', 'location', 'weather', 'music__id'], axis=1)

    def _normalize_history_data_music(self):
        music_num_frames_scaler = MinMaxScaler()
        music_frame_0_scaler = MinMaxScaler()
        music_frame_1_scaler = MinMaxScaler()
        music_frame_2_scaler = MinMaxScaler()
        music_frame_3_scaler = MinMaxScaler()
        music_frame_4_scaler = MinMaxScaler()
        music_frame_5_scaler = MinMaxScaler()
        music_frame_6_scaler = MinMaxScaler()
        one_hot_encoded_music_id = pd.get_dummies(self.normalized_history_data['music__id'], prefix='music__id')
        self.normalized_history_data = pd.concat([one_hot_encoded_music_id, self.normalized_history_data], axis=1)
        self.normalized_history_data['music__num_frames'] = music_num_frames_scaler.fit_transform(self.normalized_history_data['music__num_frames'].values.reshape(-1, 1))
        self.normalized_history_data['music__frame_0'] = music_frame_0_scaler.fit_transform(self.normalized_history_data['music__frame_0'].values.reshape(-1, 1))
        self.normalized_history_data['music__frame_1'] = music_frame_1_scaler.fit_transform(self.normalized_history_data['music__frame_1'].values.reshape(-1, 1))
        self.normalized_history_data['music__frame_2'] = music_frame_2_scaler.fit_transform(self.normalized_history_data['music__frame_2'].values.reshape(-1, 1))
        self.normalized_history_data['music__frame_3'] = music_frame_3_scaler.fit_transform(self.normalized_history_data['music__frame_3'].values.reshape(-1, 1))
        self.normalized_history_data['music__frame_4'] = music_frame_4_scaler.fit_transform(self.normalized_history_data['music__frame_4'].values.reshape(-1, 1))
        self.normalized_history_data['music__frame_5'] = music_frame_5_scaler.fit_transform(self.normalized_history_data['music__frame_5'].values.reshape(-1, 1))
        self.normalized_history_data['music__frame_6'] = music_frame_6_scaler.fit_transform(self.normalized_history_data['music__frame_6'].values.reshape(-1, 1))

    def _normalize_history_data(self):
        self.normalized_history_data = self.history_data
        self._normalize_history_data_context()
        self._normalize_history_data_username()
        self._normalize_history_data_music()
        self._drop_string_nominal_attributes()
        self.normalized_history_data.to_csv('normalized_history_data.csv', index=False)
        
    def _do_latent_clustering(self):
        print('Start clustering')
        latent_estimator = GaussianMixture(n_components=self.n_cluster, covariance_type=self.cov_type)
        latent_labels = latent_estimator.fit_predict(self.normalized_history_data)
        latent_labels = pd.DataFrame(latent_labels, columns=['latent'])
        self.history_data = pd.concat([self.history_data, latent_labels], axis=1)
        self.history_data.to_csv('concantenated_music_history.csv', index=False)

    def _calculate_recommendation_score(self):
        pass

    def get_top_thirty_recommendation(self, history_data, music_data):
        self.history_data = read_frame(history_data)
        self.music_data = read_frame(music_data)
        self._normalize_history_data()
        self._do_latent_clustering()
        self._calculate_recommendation_score()
