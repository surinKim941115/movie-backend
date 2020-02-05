import numpy as np
import pandas as pd
import json

from helper.connect_db import get_connection

GENRE_WEIGHT = 0.3


class GetMovieRecommend:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def pearsonR(self, s1, s2):

        s1_c = s1 - s1.mean()
        s2_c = s2 - s2.mean()
        return np.sum(s1_c * s2_c) / np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))

    def recommend(self, input_movie, matrix, n, similar_genre=True, meta=None):
        input_genres = meta[meta['original_title'] == input_movie]['genres'].iloc(0)[0]

        result = []
        for title in matrix.columns:
            if title == input_movie:
                continue

            # rating comparison
            cor = self.pearsonR(matrix[input_movie], matrix[title])

            # genre comparison
            if similar_genre and len(input_genres) > 0:
                temp_genres = meta[meta['original_title'] == title]['genres'].iloc(0)[0]

                same_count = np.sum(np.isin(input_genres, temp_genres))
                cor += (GENRE_WEIGHT * same_count)

            if np.isnan(cor):
                continue
            else:
                result.append((title, '{:.2f}'.format(cor), temp_genres))

        result.sort(key=lambda r: r[1], reverse=True)

        return result[:n]

    def main(self, title):
        meta = pd.read_sql("select * from movie_meta", con=self.conn)
        ratings = pd.read_sql("select * from ratings", con=self.conn)
        print(meta)
        print(ratings)

        meta = meta[['id', 'original_title', 'original_language', 'genres']]
        meta = meta.rename(columns={'id': 'movieId'})
        meta = meta[meta['original_language'] == 'en']
        ratings = ratings[['userId', 'movieId', 'rating']]
        meta.movieId = pd.to_numeric(meta.movieId, errors='coerce')
        ratings.movieId = pd.to_numeric(ratings.movieId, errors='coerce')

        meta['genres'] = meta['genres'].apply(self.parse_genres)
        meta.head()

        data = pd.merge(ratings, meta, on='movieId', how='inner')
        data.head()

        matrix = data.pivot_table(index='userId', columns='original_title', values='rating')
        matrix.head(20)

        recommend_result = self.recommend(title, matrix, 5, similar_genre=True, meta=meta)
        print(pd.DataFrame(recommend_result, columns=['Title', 'Correlation', 'Genre']))

if __name__ == '__main__':
    #
    # try:
    #     opts, args = getopt.getopt(sys.argv[1:], 't:')
    # except getopt.GetoptError as err:
    #     print(err)
    #     sys.exit(0)
    # for o, a in opts:
    #     if o == '-t':
    #         RANKING_TYPE = a
    # analysis = Analysis(pool)
    # analysis.main()
    #

    rec = GetMovieRecommend()
    rec.main("Toy Story")