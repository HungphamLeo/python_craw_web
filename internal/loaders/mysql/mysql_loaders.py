import mysql.connector

class MySQLLoader:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        self.cursor = self.conn.cursor()

    def insert_entities(self, top_entities):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS ner_entities (name TEXT, count INT)")
        for name, count in top_entities:
            self.cursor.execute("INSERT INTO ner_entities (name, count) VALUES (%s, %s)", (name, count))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()