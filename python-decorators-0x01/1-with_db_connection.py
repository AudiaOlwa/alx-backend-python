import sqlite3
import functools

# Décorateur pour gérer automatiquement la connexion à la DB
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Ouvre la connexion
        conn = sqlite3.connect('users.db')
        try:
            # Passe la connexion à la fonction
            result = func(conn, *args, **kwargs)
        finally:
            # Ferme la connexion après exécution
            conn.close()
        return result
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Exemple d'utilisation
user = get_user_by_id(user_id=1)
print(user)
