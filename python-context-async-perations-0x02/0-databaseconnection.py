import sqlite3

# Classe context manager pour gérer la connexion à la DB
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # Ouvre la connexion
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ferme la connexion
        if self.conn:
            self.conn.close()
        # Ne supprime pas l'exception si elle existe
        return False

# Utilisation du context manager
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
