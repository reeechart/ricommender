import numpy as np
import os
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
        self.n_latent_cluster = int(os.environ.get('N_LATENT_CLUSTER'))
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
        # self.normalized_history_data.to_csv('normalized_history_data.csv', index=False)
        
    def _do_latent_clustering(self):
        print('Clustering latent variable...')
        latent_estimator = GaussianMixture(n_components=self.n_latent_cluster, covariance_type=self.cov_type)
        latent_labels = latent_estimator.fit_predict(self.normalized_history_data)
        latent_labels = pd.DataFrame(latent_labels, columns=['latent'])
        self.history_data = pd.concat([self.history_data, latent_labels], axis=1)
        # self.history_data.to_csv('concantenated_music_history.csv', index=False)

    def _convert_to_probability(self, p_array):
        sum = np.sum(p_array)
        p_array = np.true_divide(p_array, sum)

        return p_array

    def _get_count_latent(self):
        count_z = np.array(self.history_data.groupby('latent').size().reset_index(name='count')['count'])

        return count_z
    
    def _get_p_latent(self):
        p_z = np.array(self.history_data.groupby('latent').size().reset_index(name='count')['count'])
        p_z = self._convert_to_probability(p_z)

        return p_z
    
    def _fill_missing_latent(self, p_array, type):
        p_full_latent = p_array
        latent_list = p_full_latent['latent'].tolist()
            
        for latent_idx in range(self.n_latent_cluster):
            if latent_idx not in latent_list:
                if (type=='p_zu' or type=='p_lz' or type=='p_wtz'):
                    p_full_latent = p_full_latent.append({'latent': latent_idx, 'count': 0}, ignore_index=True)
                elif (type=='p_wz'):
                    p_full_latent = p_full_latent.append({'latent': latent_idx, 'music__frame_0': 0, 'music__frame_1': 0, 'music__frame_2': 0, 'music__frame_3': 0, 'music__frame_4': 0, 'music__frame_5': 0, 'music__frame_6': 0}, ignore_index=True)
        
        p_full_latent = p_full_latent.sort_values('latent', ascending=True)
        return p_full_latent

    def _fill_music_missing_latent(self, p_sz):
        p_music_full_latent = p_sz
        music_ids = p_sz['music__id'].unique().tolist()

        for music_id in music_ids:
            p_single_sz = p_sz.loc[p_sz['music__id']==music_id]
            music_latent_list = p_single_sz['latent'].tolist()
            for latent_idx in range(self.n_latent_cluster):
                if latent_idx not in music_latent_list:
                    p_music_full_latent = p_music_full_latent.append({'music__id': music_id, 'latent': latent_idx, 'count': 0}, ignore_index=True)

        p_music_full_latent = p_music_full_latent.sort_values(['music__id', 'latent'], ascending=[True, True])

        return p_music_full_latent

    '''
        converts p_sz to matrix with row index as music_id and col index as latent id
        assumes that the p_sz is sorted ascendingly by music__id and latent
    '''
    def _convert_p_sz_to_latent_matrix(self, p_sz):
        p_sz = p_sz.groupby('music__id')['count'].apply(list).reset_index(name='count')
        p_sz = np.array(list(p_sz['count']))

        return p_sz

    def _get_p_latent_given_user(self):
        # get all users and its latent history count | yields dataframe
        p_zu = self.history_data.groupby(['user', 'latent']).size().reset_index(name='count')

        # get user-specific latent history indices count | yields indices of corresponding row
        p_zu_index = p_zu.index[p_zu['user']==self.user]

        # get the user-specific latent history count | yields latent and its count
        p_zu = p_zu.loc[p_zu_index][['latent', 'count']]

        p_zu = self._fill_missing_latent(p_zu, type='p_zu')

        p_zu = np.array(p_zu['count'])
        p_zu = self._convert_to_probability(p_zu)

        return p_zu

    def _get_p_music_given_latent(self):
        p_sz = self.history_data.groupby(['music__id', 'latent']).size().reset_index(name='count').sort_values('music__id', ascending=True)

        p_sz = self._fill_music_missing_latent(p_sz)
        # p_sz.to_csv('p_sz.csv')

        p_sz = self._convert_p_sz_to_latent_matrix(p_sz)
        # np.savetxt('count_sz.out', p_sz, fmt='%i')
        
        count_z = self._get_count_latent()
        # np.savetxt('count_z.out', count_z, fmt='%i')

        p_sz = np.divide(p_sz, count_z)
        # np.savetxt('p_sz.out', p_sz, fmt='%f')

        return p_sz

    def _get_p_location_given_latent(self):
        # get all location and its latent history count | yields dataframe
        p_lz = self.history_data.groupby(['location', 'latent']).size().reset_index(name='count')

        # get the corresponding location | yields indices of corresponding location
        p_lz_index = p_lz.index[p_lz['location']==self.location]

        # get the count after grouping it by latent vars | yields latent and count in location dataframe
        p_lz = p_lz.loc[p_lz_index][['latent', 'count']]

        p_lz = self._fill_missing_latent(p_lz, type='p_lz')
        p_lz = np.array(p_lz['count'])

        p_z = self._get_count_latent()

        p_lz = np.divide(p_lz, p_z)

        return p_lz

    def _get_p_weather_given_latent(self):
        # get all weather and its latent history count | yields dataframe
        p_wtz = self.history_data.groupby(['weather', 'latent']).size().reset_index(name='count')

        # get the corresponding weather data | yields indices of corresponding weather
        p_wtz_index = p_wtz.index[p_wtz['weather']==self.weather]

        # get the count after grouping it by latent vars | yields latent and count in weather dataframe
        p_wtz = p_wtz.loc[p_wtz_index][['latent', 'count']]

        p_wtz = self._fill_missing_latent(p_wtz, type='p_wtz')
        p_wtz = np.array(p_wtz['count'])

        p_z = self._get_count_latent()

        p_wtz = np.divide(p_wtz, p_z)

        return p_wtz

    def _get_p_word_given_latent(self):
        # get all audio words and its latent history sum | yields dataframe
        p_wz = self.history_data.groupby(['latent'], as_index=False).agg({'music__num_frames':'sum', 'music__frame_0':'sum', 'music__frame_1':'sum', 'music__frame_2':'sum', 'music__frame_3':'sum', 'music__frame_4':'sum', 'music__frame_5':'sum', 'music__frame_6':'sum'})

        # divide all occurences of frame with total frame
        latent = p_wz['latent'].to_frame()
        p_wz = p_wz[['music__frame_0', 'music__frame_1', 'music__frame_2', 'music__frame_3', 'music__frame_4', 'music__frame_5', 'music__frame_6']].div(p_wz['music__num_frames'], axis=0)
        p_wz = pd.concat([latent, p_wz], axis=1)

        p_wz = self._fill_missing_latent(p_wz, type='p_wz')
        p_wz = p_wz.drop('latent', axis=1)
        p_wz = np.array(p_wz)
        # np.savetxt('p_wz.out', p_wz)

        return p_wz

    def _combine_music_recommendation_score(self, music_score):
        self.music_data['score'] = music_score

    def _calculate_recommendation_score(self):
        print('Calculating recommendation...')
        p_z = self._get_p_latent()
        p_zu = self._get_p_latent_given_user()
        p_lz = self._get_p_location_given_latent()
        p_wtz = self._get_p_weather_given_latent()
        p_wz = self._get_p_word_given_latent()
        p_sz = self._get_p_music_given_latent()

        np.savetxt('p_sz.out', p_sz, fmt='%f')
        np.savetxt('p_z.out', p_z, fmt='%f')
        np.savetxt('p_zu.out', p_zu, fmt='%f')
        np.savetxt('p_lz.out', p_lz, fmt='%f')
        np.savetxt('p_wtz.out', p_wtz, fmt='%f')

        p_uslwtw = np.multiply(p_sz, p_z)
        p_uslwtw = np.multiply(p_uslwtw, p_zu)
        p_uslwtw = np.multiply(p_uslwtw, p_lz)
        p_uslwtw = np.multiply(p_uslwtw, p_wtz)
        p_uslwtw = np.matmul(p_uslwtw, p_wz)
        p_uslwt = np.sum(p_uslwtw, axis=1)

        p_s_given_ulwt = self._convert_to_probability(p_uslwt)

        self._combine_music_recommendation_score(p_s_given_ulwt)

        # print('this is p_z')
        # print(p_z)
        # print(p_z.shape)
        # print('this is p_zu')
        # print(p_zu)
        # print(p_zu.shape)
        # print('this is p_lz')
        # print(p_lz)
        # print(p_lz.shape)
        # print('this is p_wtz')
        # print(p_wtz)
        # print(p_wtz.shape)
        # print('this is p_wz')
        # print(p_wz)
        # print(p_wz.shape)
        # print('this is p_sz')
        # print(p_sz)
        # print(p_sz.shape)
        # print('this is p_uslwtw')
        # print(p_uslwtw)
        # print(p_uslwtw.shape)
        # np.savetxt('p_uslwtw.out', p_uslwtw, fmt='%.18e')

    def _sort_music_based_on_score(self):
        self.music_data = self.music_data.sort_values('score', ascending=False)

    def get_top_thirty_recommendation(self, history_data, music_data):
        self.history_data = read_frame(history_data)
        self.music_data = read_frame(music_data)
        self._normalize_history_data()
        self._do_latent_clustering()
        self._calculate_recommendation_score()
        self._sort_music_based_on_score()
        self.music_data.to_csv('music_score.csv', index=False)
