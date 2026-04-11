import psycopg2
from psycopg2.extras import DictCursor
import os
from urllib.parse import urlparse

class AnalyzerRepo:
    def __init__(self):
        pass

    def get_connection(self):
        """Создает НОВОЕ соединение с БД для каждого запроса"""
        DATABASE_URL = os.getenv('DATABASE_URL')
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is not set")
        
        parsed = urlparse(DATABASE_URL)
        
        # Параметры подключения
        conn_params = {
            'dbname': parsed.path[1:],
            'user': parsed.username,
            'password': parsed.password,
            'host': parsed.hostname,
            'port': parsed.port or 5432,
            'connect_timeout': 10,
        }
        
        # Настройка SSL для Render
        if 'render.com' in parsed.hostname:
            conn_params['sslmode'] = 'require'
        else:
            conn_params['sslmode'] = 'disable'
        
        return psycopg2.connect(**conn_params)

    def get_urls(self):
        conn = self.get_connection()
        try: 
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM urls ORDER BY created_at DESC;")
                return [dict(row) for row in cur]
        finally:
            conn.close()
    
    def add_url(self, url):
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id', (url,))
                url_id = cur.fetchone()['id']
            conn.commit()
            return url_id
        finally:
            conn.close()
    
    def add_url_if_not_exists(self, url):
        conn = self.get_connection()
        try:
            return self.add_url(url)
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            return self.get_id_by_name(url)
        finally:
            conn.close()

    def get_url_info(self, id):
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('SELECT * FROM urls WHERE id = (%s)', (id,))
                return dict(cur.fetchone()) if cur.rowcount > 0 else None
        finally:
            conn.close()
        
    def get_id_by_name(self, url):
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('SELECT id FROM urls WHERE name = %s', (url,))
                url_id = cur.fetchone()['id']
                return url_id
        finally:
            conn.close()