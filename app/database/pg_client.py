import psycopg2
from psycopg2.extras import RealDictCursor
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

def get_pg_connection():
    """
    Establishes an atomic transaction wire to the local PostgreSQL server container.
    Port 5433 isolates containerized traffic from native local Windows engine background services.
    """
    return psycopg2.connect(
        host="127.0.0.1",
        database="enterprise_erp",
        user="postgres",
        password="postgrespassword",
        port=5433 # FIXED: Routes directly to the containerized database layout
    )


def init_postgres_ledger():
    """Generates the transactional ledger table infrastructure."""
    conn = get_pg_connection()
    cur = conn.cursor()
    
    # Create enterprise ERP systems table registry
    cur.execute("""
        CREATE TABLE IF NOT EXISTS erp_ledger (
            po_number VARCHAR(50) PRIMARY KEY,
            vendor_name VARCHAR(100) NOT NULL,
            authorized_amount NUMERIC(12, 2) NOT NULL
        );
    """)
    
    # Inject baseline golden records for verification profiling
    cur.execute("""
        INSERT INTO erp_ledger (po_number, vendor_name, authorized_amount)
        VALUES 
            ('PO-9901', 'Acme Corp', 1500.00),
            ('PO-9902', 'Delta Labs', 420.50),
            ('PO-9903', 'Vertex Media', 8900.00)
        ON CONFLICT (po_number) DO NOTHING;
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def query_postgres_erp(po_number: str) -> dict:
    """Queries Postgres to verify line-item authorization details."""
    conn = get_pg_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM erp_ledger WHERE po_number = %s;", (po_number,))
    record = cur.fetchone()
    cur.close()
    conn.close()
    return record

async def get_async_pg_pool():
    """Generates a high-performance asynchronous connection pool for high-throughput stress tests."""
    return await asyncpg.create_pool(
        host="127.0.0.1",
        database="enterprise_erp",
        user="postgres",
        password="postgrespassword",
        port=5433,
        min_size=10,
        max_size=50
    )