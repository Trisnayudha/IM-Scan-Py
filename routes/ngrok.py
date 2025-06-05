


from flask import Blueprint, jsonify, request
# Adjust the following import to your actual DB helper/module
from extensions import get_db_connection

ngrok_bp = Blueprint('ngrok_bp', __name__)

@ngrok_bp.route('/ngrok', methods=['GET'])
def get_all_ngrok():
    """
    Retrieve all records from the ngrok table.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, link, type, created_at, updated_at FROM ngrok")
    rows = cur.fetchall()
    conn.close()

    ngrok_list = []
    for row in rows:
        ngrok_list.append({
            'id': row[0],
            'link': row[1],
            'type': row[2],
            'created_at': row[3].isoformat() if row[3] else None,
            'updated_at': row[4].isoformat() if row[4] else None
        })

    return jsonify({'status': 1, 'data': ngrok_list})

@ngrok_bp.route('/ngrok/<int:ngrok_id>', methods=['GET'])
def get_ngrok_by_id(ngrok_id):
    """
    Retrieve a single ngrok record by its ID.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, link, type, created_at, updated_at FROM ngrok WHERE id = %s",
        (ngrok_id,)
    )
    row = cur.fetchone()
    conn.close()

    if row:
        ngrok_data = {
            'id': row[0],
            'link': row[1],
            'type': row[2],
            'created_at': row[3].isoformat() if row[3] else None,
            'updated_at': row[4].isoformat() if row[4] else None
        }
        return jsonify({'status': 1, 'data': ngrok_data})
    else:
        return jsonify({'status': 0, 'message': 'Record not found'}), 404