import sqlite3, time

DB_NAME = "nve.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            key TEXT PRIMARY KEY,
            value TEXT,
            sources TEXT,
            last_updated INTEGER,
            confidence REAL
        )
    """)
    conn.commit()
    conn.close()
    print("Nexus Veritas database created successfully!")

if __name__ == "__main__":
    init_db()
