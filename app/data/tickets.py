from app.data.db import get_conn

def add_ticket(requester: str, assigned_to: str = None, status: str = "open", steps: int = 1):
    conn = get_conn()
    conn.execute(
        "INSERT INTO it_tickets (requester, assigned_to, status, steps) VALUES (?, ?, ?, ?)",
        (requester, assigned_to, status, steps)
    )
    conn.commit()
    conn.close()

def list_tickets(limit=200):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, requester, assigned_to, status, steps, created_at, resolved_at FROM it_tickets ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_ticket(ticket_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM it_tickets WHERE id = ?", (ticket_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def update_ticket(ticket_id: int, requester: str, assigned_to: str, status: str, steps: int, resolved_at = None):
    conn = get_conn()
    conn.execute(
        "UPDATE it_tickets SET requester = ?, assigned_to = ?, status = ?, steps = ?, resolved_at = ? WHERE id = ?",
        (requester, assigned_to, status, steps, resolved_at, ticket_id)
    )
    conn.commit()
    conn.close()

def delete_ticket(ticket_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM it_tickets WHERE id = ?", (ticket_id,))
    conn.commit()
