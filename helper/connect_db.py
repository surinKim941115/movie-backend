import os
import sys

print("connection", sys.path)
import pymysql
from helper.aws_helper import get_secret
import json


def get_connection(db_name='moviedata'):
    db_info = json.loads(get_secret()['SecretString'])

    conn = pymysql.connect(host=db_info['host'],
                            port=db_info['port'],
                            user=db_info['username'],
                            passwd=db_info['password'],
                            db=db_name,
                            cursorclass=pymysql.cursors.DictCursor,
                            charset='utf8')

    return conn

