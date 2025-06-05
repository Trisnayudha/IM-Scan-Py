# routes/scan_qr.py
from flask import Blueprint, request, jsonify
from utils.ticket_mapper import map_ticket_type
from datetime import datetime
from extensions import get_db_connection

scan_qr_bp = Blueprint('scan_qr', __name__)

@scan_qr_bp.route('/scan-qr', methods=['POST'])
def scan_qr():
    data = request.get_json() or {}
    code_payment = data.get('code_payment')
    day = data.get('day')
    if not code_payment or not day:
        return jsonify({"status": 0, "message": "code_payment and day are required", "data": None}), 400
    try:
        # Parse the day parameter (ISO or Indonesian format) and map to checkin_day field
        col = None
        try:
            date_str = day.lower()
            if '-' in date_str:
                dt = datetime.fromisoformat(day)
            else:
                months = {
                    'januari':1, 'februari':2, 'maret':3, 'april':4, 'mei':5,
                    'juni':6, 'juli':7, 'agustus':8, 'september':9,
                    'oktober':10, 'november':11, 'desember':12
                }
                parts = date_str.split()
                year = int(parts[0])
                month = next(v for k,v in months.items() if k in date_str)
                day_num = int(parts[-1])
                dt = datetime(year, month, day_num)
            # Map specific dates in June 2025 to date_day fields
            if dt.year == 2025 and dt.month == 6:
                if dt.day == 10:
                    col = 'date_day1'
                elif dt.day == 11:
                    col = 'date_day2'
                elif dt.day == 12:
                    col = 'date_day3'
        except Exception:
            return jsonify({"status": 0, "message": "Invalid day format", "data": None}), 400
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id AS payment_id, u.name, u.job_title, u.company_name, et.category, et.title, et.type
            FROM payment p
            JOIN users u ON u.id = p.users_id
            JOIN events_tickets et ON et.id = p.package_id
            WHERE p.code_payment = %s AND p.aproval_quota_users = 1
        """, (code_payment,))
        row = cur.fetchone()
        if row:
            payment_id, name, job_title, company, category, title, type_val = row
            # Validate ticket category against the check-in day
            if col:
                if dt.day == 10 and category not in ('Day 1 Access', 'All Access'):
                    return jsonify({
                        "status": 0,
                        "message": "Oops! Your ticket only grants Day 1 Access. You cannot check in today."
                    }), 403
                if dt.day == 11 and category not in ('Day 2 Access', 'All Access'):
                    return jsonify({
                        "status": 0,
                        "message": "Oops! Your ticket only grants Day 2 Access. You cannot check in today."
                    }), 403
                if dt.day == 12 and category not in ('Day 3 Access', 'All Access'):
                    return jsonify({
                        "status": 0,
                        "message": "Oops! Your ticket only grants Day 3 Access. You cannot check in today."
                    }), 403
            # Fetch image associated with this payment_id
            cur.execute("SELECT image FROM users_delegate WHERE payment_id = %s", (payment_id,))
            img_row = cur.fetchone()
            image = img_row[0] if img_row else None
            if image:
                # Build full URL using the host URL; strip trailing slash to avoid duplication
                base_url = request.host_url.rstrip('/')
                image_url = f"{base_url}/{image}"
            else:
                image_url = None
            # Update check-in timestamp for the delegate in the users_delegate table
            if col:
                update_query = f"UPDATE users_delegate SET {col} = NOW() WHERE payment_id = %s"
                cur.execute(update_query, (payment_id,))
                conn.commit()
            conn.close()
            ticket_label, ticket_color = map_ticket_type(type_val, title)
            return jsonify({
                "status": 1,
                "message": "Scan QR successful",
                "data": {
                    "name": name,
                    "job_title": job_title,
                    "company": company,
                    "code_payment": code_payment,
                    "checkin_field": col,
                    "ticket_type": ticket_label,
                    "ticket_color": ticket_color,
                    "image": image_url
                }
            })
        else:
            conn.close()
            return jsonify({"status": 0, "message": "Delegate not found", "data": None}), 404
    except Exception as e:
        return jsonify({"status": 0, "message": str(e), "data": None}), 500
