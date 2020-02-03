import os
import sys
import json
# here = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(os.path.join(here, "vendor"))
print(sys.path)
from helper.connect_db import get_connection


class GetPopularData:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def main(self):
        select_query = """
            SELECT tmdb_id, title, poster_path, backdrop_path, overview,  release_date
            FROM popular_movie
        """

        self.cursor.execute(select_query)
        result = self.cursor.fetchall()
        result = {'data': result}
        print(result)
        return result


def run(event, context):
    get_popular_data = GetPopularData()
    response = get_popular_data.main()
    result = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response)
        }

    return result


if __name__ == '__main__':
    gpd = GetPopularData()
    gpd.main()