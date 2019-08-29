"""
@File    : co_filtering.py
@Time    : 2019/8/29 12:22
@Author  : tangwenpan
"""

from data_helper import DataSet
from math import sqrt


class CoFiltering:

    def __init__(self):
        self.data = DataSet()

    def pearson_sim(self, user1, user2):
        """
        Calculate Pearson-Correlation-Coefficient of user1 & user2.
        """
        user1_array = self.data.matrix[user1 - 1]
        user2_array = self.data.matrix[user2 - 1]
        length = len(user1_array)
        sum1 = sum(user1_array)
        sum2 = sum(user2_array)
        sum_mul = self.multi(user1_array, user2_array)
        sum_x2 = sum([i ** 2 for i in user1_array])
        sum_y2 = sum([j ** 2 for j in user2_array])
        num = sum_mul - (float(sum1) * float(sum2) / length)
        den = sqrt((sum_x2 - float(sum1 ** 2) / length) * (sum_y2 - float(sum2 ** 2) / length))
        return num / den

    @staticmethod
    def multi(x, y):
        """
        To get two 1D-arrays' multiply result.
        The two arrays must have the same size.
        :param x: one array.
        :param y: another array.
        :return: multiply result.
        """
        result = 0.
        for i in range(len(x)):
            result += x[i] * y[i]
        return result

    def most_similar(self, user1, top_n=5):
        """
        To find TOP_N most similar users.
        :param user1: user_id, NOT ARRAY, eg. 23
        :param top_n: Just like what "TOP_N" said.
        :return: LIKE "[(most_similar_user_1, score),...(most_similar_user_topN, score)]".
        """
        result_collect = {}
        for user2 in self.data.users:
            if user2 == user1:
                pass
            else:
                try:
                    result = self.pearson_sim(user1, user2)
                    result_collect[user2] = result
                except IndexError:
                    pass

        results_sorted = sorted(result_collect.items(), key=lambda item: item[1], reverse=True)[:top_n]
        print('Most similar users: {}'.format(' | '.join([str(x[0]) for x in results_sorted])))
        return results_sorted

    def predict(self, user, top_n=5, recommend_num=5):
        if user not in self.data.users:
            raise ValueError('Cannot find user "{}", please check.'.format(user))

        results = self.most_similar(user, top_n)
        recommend = []
        for user_id, val in results:
            diff_list = list(self.data.matrix[user_id] - self.data.matrix[user])
            temp = filter(lambda x: x[1] > 0, enumerate(diff_list))
            recommend.extend(temp)
        recommend = sorted(recommend, key=lambda x: x[1], reverse=True)

        movie_list = []
        while True:
            for i in range(1, 6).__reversed__():
                temp_list = filter(lambda x: x[1] == i, recommend)
                temp_list = sorted(temp_list, key=lambda x: self.data.move_pop_rank[x[0]], reverse=True)
                movie_list.extend([x[0] + 1 for x in temp_list])
                if len(movie_list) >= recommend_num:
                    break
                else:
                    continue
            break
        movie_list = [self.data.id2movie(x) for x in movie_list[:recommend_num]]
        print('Recommend movies: {}'.format(' | '.join(movie_list)))


if __name__ == "__main__":
    cf = CoFiltering()
    cf.predict(5342, 5, 5)
