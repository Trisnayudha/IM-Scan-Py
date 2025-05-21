from flask import Blueprint, request, jsonify
from extensions import get_db_connection
from utils.ticket_mapper import map_ticket_type

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
            SELECT u.name, u.job_title, u.company_name, p.code_payment, et.title, et.type
            FROM payment p
            JOIN users u ON u.id = p.users_id
            JOIN events_tickets et ON et.id = p.package_id
            WHERE (u.name LIKE %s OR u.company_name LIKE %s) AND p.aproval_quota_users = 1 AND p.events_id = 13
            LIMIT 20
        """, (like_pattern, like_pattern))
        rows = cur.fetchall()
        conn.close()
        data = []
        for r in rows:
            ticket_label, ticket_color = map_ticket_type(r[5], r[4])
            data.append({
                "name": r[0],
                "job_title": r[1],
                "company": r[2],
                "code_payment": r[3],
                "checkin_field": None,
                "ticket_type": ticket_label,
                "ticket_color": ticket_color
            })
        return jsonify({"status": 1, "message": "Success", "data": data})
    except Exception as e:
        return jsonify({"status": 0, "message": str(e), "data": []}), 500
