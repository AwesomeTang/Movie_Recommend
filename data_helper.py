"""
@File    : data_helper.py
@Time    : 2019/8/29 11:05
@Author  : tangwenpan
"""

import numpy as np
import Config


class DataSet:

    def __init__(self):
        self.matrix, self.movie_map, self.users = self.rating_matrix()
        self.data_reader()

        # a function that helps to convert movie-id into movie-name.
        self.id2movie = lambda idx: self.movie_map[str(idx)]

        self.move_pop_rank = self.most_pop_movie()

    def data_reader(self):
        """
        Read rating file and fill self.matrix with rate.
        """
        with open(Config.rating_data_path, 'rb') as f:
            for line in f.readlines():
                try:
                    item_list = line.decode('utf-8').strip('\n').split('::')
                    self.matrix[int(item_list[0]) - 1, int(item_list[1]) - 1] = item_list[2]
                except UnicodeDecodeError:
                    pass
                except IndexError:
                    pass

    @staticmethod
    def rating_matrix():
        """
        :return:
        data_matrix: is an empty matrix(actually is filled by zeros.) which has size [users' num * movies' num'].
        movies: is a dictionary which key is movie-id and value is movie name.
        users: is a list, all the user-ids' collection.
        """
        movies = {}
        with open(Config.movies_data_path, 'rb') as f:
            f_lines = f.readlines()
            movies_counter = len(f_lines)
            for line in f_lines:
                try:
                    movie_id, movie_name, genres = line.decode('utf-8').strip('\n').split('::')
                    movies[movie_id] = movie_name
                except UnicodeDecodeError:
                    pass

        users = []
        with open(Config.users_data_path, 'rb') as f:
            f_lines = f.readlines()
            users_counter = len(f_lines)
            for line in f_lines:
                try:
                    user, _, _, _, _ = line.decode('utf-8').strip('\n').split('::')
                    users.append(int(user))
                except UnicodeDecodeError:
                    pass
        data_matrix = np.zeros([users_counter, movies_counter])
        return data_matrix, movies, users

    def movie_rated(self, user_id):
        """
        :return: all movies' name that have been rated by USER-ID.
        """
        user_array = list(self.matrix[user_id - 1])
        rated = []
        for i, rate in enumerate(user_array):
            if rate > 0:
                rated.append(self.id2movie(i+1))
        print('User[{}] rated movie: {}'.format(user_id, ' | '.join(rated)))

    def most_pop_movie(self):
        """
        Calculate every movie's average rate.
        :return: a dictionary, key is movie-id, value is movie-rate.
        """
        movie_rate_sum = list(np.mean(self.matrix, axis=0))
        movie_rank = sorted(enumerate(movie_rate_sum), key=lambda x: x[1], reverse=True)
        return dict(movie_rank)


if __name__ == "__main__":
    data = DataSet()
    data.movie_rated(5342)
