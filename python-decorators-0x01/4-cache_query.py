import time
import sqlite3
import functools

# Dictionnaire global pour stocker les résultats en cache
query_cache = {}

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

# Décorateur pour mettre en cache les résultats des requêtes SQL
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Récupère la requête SQL
        query = kwargs.get('query') if 'query' in kwargs else args[1] if len(args) > 1 else None
        if query is None:
            return func(*args, **kwargs)

        # Si la requête est déjà dans le cache, retourne le résultat
        if query in query_cache:
            print("[CACHE] Résultat récupéré depuis le cache")
            return query_cache[query]

        # Sinon, exécute la fonction et met le résultat en cache
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("[CACHE] Résultat mis en cache")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Premier appel, le résultat est mis en cache
users = fetch_users_with_cache(query="SELECT * FROM users")

# Deuxième appel, le résultat provient du cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
