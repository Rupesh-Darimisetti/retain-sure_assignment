import sqlite3
from config import DATABSE

def get_db_connection():
    conn = sqlite3.connect(DATABSE,check_same_thread=False)
    return conn