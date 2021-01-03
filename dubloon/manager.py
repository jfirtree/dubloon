import sqlite3


class Dubloon:
    def __init__(self):
        self.db_path = '../test.db'

    def query(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM transactions')
        print(cursor.fetchone())


if __name__ == '__main__':
    d = Dubloon()
    d.query()
