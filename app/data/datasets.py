from app.data.db import get_conn

def add_dataset(name: str, rows: int, cols: int):
    conn = get_conn()
    conn.execute(
        "INSERT INTO datasets_metadata (name, rows, cols) VALUES (?, ?, ?)",
        (name, rows, cols)
    )
    conn.commit()
    conn.close()

def list_datasets(limit=200):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, rows, cols, imported_at FROM datasets_metadata ORDER BY imported_at DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_dataset(dataset_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM datasets_metadata WHERE id = ?", (dataset_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def update_dataset(dataset_id: int, name: str, rows: int, cols: int):
    conn = get_conn()
    conn.execute(
        "UPDATE datasets_metadata SET name = ?, rows = ?, cols = ? WHERE id = ?",
        (name, rows, cols, dataset_id)
    )
    conn.commit()
    conn.close()

def delete_dataset(dataset_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
    conn.commit()
    conn.close()
