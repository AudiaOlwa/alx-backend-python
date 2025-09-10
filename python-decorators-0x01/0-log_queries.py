import sqlite3
import functools
from datetime import datetime  # <-- Ajouté pour le test

# Décorateur pour logger les requêtes SQL
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query:
            # Logue la requête avec l'heure actuelle
            print(f"[{datetime.now()}] Exécution de la requête SQL : {query}")
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

# Exemple d'utilisation
users = fetch_all_users(query="SELECT * FROM users")
print(users)
