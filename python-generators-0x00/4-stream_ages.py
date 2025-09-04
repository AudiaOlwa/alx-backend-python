#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:  # ✅ un seul loop ici
        yield row["age"]

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Uses the age generator to compute average age in a memory-efficient way.
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # ✅ deuxième loop
        total += age
        count += 1

    if count == 0:
        print("No users found")
    else:
        avg = total / count
        print(f"Average age of users: {avg:.2f}")
