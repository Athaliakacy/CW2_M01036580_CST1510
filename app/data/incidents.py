from app.data.db import get_conn

def add_incident(title: str, category: str, severity: int):
    conn = get_conn()
    conn.execute(
        "INSERT INTO cyber_incidents (title, category, severity) VALUES (?, ?, ?)",
        (title, category, severity)
    )
    conn.commit()
    conn.close()

def list_incidents(limit=200):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, category, severity, created_at FROM cyber_incidents ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_incident(incident_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents WHERE id = ?", (incident_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def update_incident(incident_id: int, title: str, category: str, severity: int):
    conn = get_conn()
    conn.execute(
        "UPDATE cyber_incidents SET title = ?, category = ?, severity = ? WHERE id = ?",
        (title, category, severity, incident_id)
    )
    conn.commit()
    conn.close()

def delete_incident(incident_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    conn.close()
