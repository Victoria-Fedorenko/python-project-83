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
            cur.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id', (url,))
            url_id = cur.fetchone()['id']
        self.conn.commit()
        return url_id
    
    def add_url_if_not_exists(self, url):
        try:
            return self.add_url(url)
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return self.get_id_by_name(url)

    def get_url_info(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE id = (%s)', (id,))
            return dict(cur.fetchone()) if cur.rowcount > 0 else None
        
    def get_id_by_name(self, url):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT id FROM urls WHERE name = %s', (url,))
            url_id = cur.fetchone()['id']
            return url_id