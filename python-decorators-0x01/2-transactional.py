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

# Décorateur pour gérer les transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # commit si tout va bien
            print("[TRANSACTION] Commit effectué")
            return result
        except Exception as e:
            conn.rollback()  # rollback si erreur
            print(f"[TRANSACTION] Rollback effectué à cause de l'erreur : {e}")
            raise  # remonte l'erreur
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Exemple d'utilisation
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
