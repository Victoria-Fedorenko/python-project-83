import psycopg2
from psycopg2.extras import DictCursor

class AnalyzerRepo:
    def __init__(self, conn):
        self.conn = conn

    def get_urls(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls")
            return [dict(row) for row in cur]
    
    def add_url(self, url):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('INSERT INTO urls (name) VALUES (%s)', (url['name'],))
        self.conn.commit()

    def get_url_info(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE id = (%s)', (id,))
            return dict(cur.fetchone()) if cur.rowcount > 0 else None