import os
import asyncpg
from pgvector.asyncpg import Vector

DATABASE_URL = os.getenv('DATABASE_URL')

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    # Ensure pgvector extension and table
    await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            embedding VECTOR(1536)
        );
        """
    )
    await conn.close()

async def add_ticket(content: str, embedding: list[float]):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(
        "INSERT INTO tickets(content, embedding) VALUES($1, $2);",
        content, Vector(embedding)
    )
    await conn.close()

async def search_tickets(query_vec: list[float], limit: int = 5):
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch(
        "SELECT id, content, embedding <=> $1 AS distance"
        " FROM tickets ORDER BY embedding <=> $1 LIMIT $2;",
        Vector(query_vec), limit
    )
    await conn.close()
    return rows