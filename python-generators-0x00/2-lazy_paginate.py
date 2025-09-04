#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """Fetch a batch of users from the database with LIMIT and OFFSET"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator to lazily paginate through user_data.
    It fetches the next page only when needed.
    """
    offset = 0
    while True:  # single loop, fetch one page at a time
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        yield rows
        offset += page_size
