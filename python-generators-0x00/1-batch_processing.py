#!/usr/bin/python3
from typing import List, Dict
import sqlite3


def stream_users_in_batches(batch_size: int):
    """Generator: fetch users in batches of batch_size"""
    conn = sqlite3.connect("user_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(dict(row))
        if len(batch) == batch_size:
            yield batch
            batch = []

    # Yield any remaining rows
    if batch:
        yield batch

    conn.close()

def batch_processing(batch_size):
    """Process batches: filter users age > 25 using yield"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                yield user