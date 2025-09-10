import asyncio
import aiosqlite

# Fonction asynchrone pour récupérer tous les utilisateurs
async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            return results

# Fonction asynchrone pour récupérer les utilisateurs de plus de 40 ans
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            return results

# Fonction principale pour exécuter les deux requêtes simultanément
async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("Tous les utilisateurs:")
    print(all_users)
    print("\nUtilisateurs de plus de 40 ans:")
    print(older_users)

# Exécution du code
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
