import sqlite3
import functools

# Décorateur pour logger les requêtes SQL
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Récupère la requête SQL passée en argument
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query:
            print(f"[LOG] Exécution de la requête SQL : {query}")
        # Appelle la fonction originale
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


