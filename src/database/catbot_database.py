import psycopg2
import urllib.parse as urlparse
import os

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
       if cls not in instances:
            instances[cls] = cls(*args, **kw)
       return instances[cls]
    return _singleton

@singleton
class CatbotDatabase(object):
    def connect(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()
        self.cursor.close()

    def commit(self):
        self.conn.commit()
