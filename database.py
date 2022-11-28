import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        cur = self.conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS store (frequency FLOAT, permittivity FLOAT, conductivity FLOAT, loss_ratio FLOAT )")
        self.conn.commit()
        self.conn.close()

    def insert(self, frequency, permittivity, conductivity, loss_ratio):
        self.conn = sqlite3.connect("database.db")
        cur = self.conn.cursor()
        cur.execute("INSERT INTO store VALUES(?,?,?,?)", (frequency, permittivity, conductivity, loss_ratio))
        self.conn.commit()
        self.conn.close()

    def view(self):
        self.conn = sqlite3.connect("database.db")
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM store")
        self.rows = cur.fetchall()
        self.conn.close()
        return self.rows

    def delete(self, frequency):
        self.conn = sqlite3.connect("database.db")
        cur = self.conn.cursor()
        cur.execute("DELETE FROM store WHERE frequency=?", (frequency,))
        self.conn.commit()
        self.conn.close()

    def update(self, permittivity, conductivity, loss_ratio, frequency):
        self.conn = sqlite3.connect("database.db")
        cur = self.conn.cursor()
        cur.execute("UPDATE store SET permittivity=?, conductivity=?, loss_ratio=?  WHERE frequency=?",
                    (permittivity, conductivity, loss_ratio, frequency))
        self.conn.commit()
        self.conn.close()

