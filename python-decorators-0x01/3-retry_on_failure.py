import time
import sqlite3
import functools

# Décorateur pour gérer la connexion à la DB
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# Décorateur pour réessayer en cas d'erreur
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"[RETRY] Erreur détectée : {e}. Tentative {attempt}/{retries}. Reprise dans {delay}s...")
                    time.sleep(delay)
            # Si toutes les tentatives échouent, on relance l'exception
            raise Exception(f"Échec après {retries} tentatives.")
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Exemple d'utilisation
users = fetch_users_with_retry()
print(users)
