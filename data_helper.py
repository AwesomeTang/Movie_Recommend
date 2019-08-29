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

        self.id2movie = lambda idx: self.movie_map[str(idx)]

    def data_reader(self):
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


if __name__ == "__main__":
    data = DataSet()
    print(data.matrix[0, 1192])
    print(data.id2movie(2222))
