# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL murlings
# - Tracking click counts
# - Managing URL metadata
from datetime import datetime
from app.database.db import get_db_connection

def insert_url(short_code,original_url):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO urls (short_code, original_url) VALUES (?,?)',
        (short_code, original_url)
    )
    conn.commit()
    conn.close()

def get_url(short_code):
    conn = get_db_connection()
    url = conn.execute('SELECT * FROM urls WHERE short_code = ?', (short_code,)).fetchone()
    conn.close()
    print(url)
    return url

def increment_click_count(short_code):
    conn = get_db_connection()
    conn.execute(
        'UPDATE urls SET click_count=click_count+1 WHERE short_code = ?',
        (short_code)
    )
    conn.commit()
    conn.close()

