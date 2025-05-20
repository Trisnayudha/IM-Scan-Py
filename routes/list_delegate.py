from flask import Blueprint, request, jsonify
from extensions import get_db_connection

list_delegate_bp = Blueprint('list_delegate', __name__)

@list_delegate_bp.route('/list-delegate', methods=['GET'])
def list_delegate():
    search = request.args.get('search', '')
    if len(search) < 4:
        return jsonify({"status": 0, "message": "Search term must be at least 4 characters", "data": []}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        like_pattern = f"%{search}%"
        cur.execute("""
            SELECT u.name, u.company_name, p.code_payment
            FROM payment p
            JOIN users u ON u.id = p.users_id
            WHERE (u.name LIKE %s OR u.company_name LIKE %s) AND p.aproval_quota_users = 1 AND p.events_id = 13
            LIMIT 20
        """, (like_pattern, like_pattern))
        rows = cur.fetchall()
        conn.close()
        data = [{"name": r[0], "company_name": r[1], "code_payment": r[2]} for r in rows]
        return jsonify({"status": 1, "message": "Success", "data": data})
    except Exception as e:
        return jsonify({"status": 0, "message": str(e), "data": []}), 500
