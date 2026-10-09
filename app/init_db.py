from app.database import get_connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL
                    CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH')),
                status TEXT NOT NULL DEFAULT 'OPEN'
                    CHECK (status IN ('OPEN', 'CLOSED'))
            )
        """)


if __name__ == "__main__":
    init_db()
    print("Datenbanktabelle ist bereit.")