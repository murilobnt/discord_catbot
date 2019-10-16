import random

from psycopg2.extensions import AsIs
from src.database.catbot_database import CatbotDatabase

class TemplateApplier:
    def __init__(self):
        self.cb_d = CatbotDatabase()

    def connect_db(self):
        self.cb_d.connect()
        self.cursor = self.cb_d.cursor

    def close_db_connection(self):
        self.cb_d.close()

    def get_random_noun(self, field = "value"):
        self.cursor.execute("SELECT %s FROM nouns ORDER BY RANDOM() LIMIT 1", (AsIs(field),))
        return str(self.cursor.fetchone()[0])

    def get_random_adjective(self, field = "value"):
        self.cursor.execute("SELECT %s FROM adjectives ORDER BY RANDOM() LIMIT 1", (AsIs(field),))
        return str(self.cursor.fetchone()[0])

    def get_random_adverb(self, field = "value"):
        self.cursor.execute("SELECT %s FROM adverbs ORDER BY RANDOM() LIMIT 1", (AsIs(field),))
        return str(self.cursor.fetchone()[0])

    def get_random_t_verb(self, field = "value"):
        self.cursor.execute("SELECT %s FROM verbs WHERE type='transitive' ORDER BY RANDOM() LIMIT 1", (AsIs(field),))
        return str(self.cursor.fetchone()[0])

    def get_random_i_verb(self, field = "value"):
        self.cursor.execute("SELECT %s FROM verbs WHERE type='intransitive' ORDER BY RANDOM() LIMIT 1", (AsIs(field),))
        return str(self.cursor.fetchone()[0])
