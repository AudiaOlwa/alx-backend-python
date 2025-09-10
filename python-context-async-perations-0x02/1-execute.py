import sqlite3

# Classe context manager pour exécuter une requête SQL
class ExecuteQuery:
    def __init__(self, query, params=None, db_name='users.db'):
        self.query = query
        self.params = params if params else ()
        self.db_name = db_name
        self.conn = None
        self.results = None

    def __enter__(self):
        # Ouvre la connexion et exécute la requête
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results  # retourne les résultats directement

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        # Ne supprime pas l'exception si elle existe
        return False

# Utilisation du context manager
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as results:
    print(results)
