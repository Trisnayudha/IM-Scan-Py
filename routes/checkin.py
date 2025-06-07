# routes/checkin.py
from flask import Blueprint, request, jsonify
from extensions import get_db_connection
import requests
import os
import base64
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# Thread pool for asynchronous tasks
executor = ThreadPoolExecutor(max_workers=4)

checkin_bp = Blueprint('checkin', __name__)

@checkin_bp.route('/checkin', methods=['POST'])
def checkin():
    data = request.get_json()
    code_payment = data.get('code_payment')
    link_webhook = data.get('link_webhook')
    day = data.get('day')
    name = data.get('name')
    job = data.get('job_title')
    company = data.get('company')
    image = data.get('image')
    if not code_payment or not link_webhook or not day:
        return jsonify({"status": 0, "message": "code_payment, link_webhook, and day are required", "data": None}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor(buffered=True)
        cur.execute("""
            SELECT p.id, ud.id
            FROM payment p
            JOIN users_delegate ud ON ud.users_id = p.users_id AND ud.events_id = p.events_id
            WHERE p.code_payment = %s AND p.aproval_quota_users = 1
        """, (code_payment,))
        result = cur.fetchone()

        if not result:
            return jsonify({"status": 0, "message": "QR Code tidak valid", "data": None})

        payment_id, delegate_id = result

        # Determine which checkin_day column based on the provided day
        try:
            date_str = day.lower()
            if '-' in date_str:
                dt = datetime.fromisoformat(day)
            else:
                # Parse Indonesian format like "2025 juni tanggal 10"
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
            col = None
            # Map specific dates in June 2025 directly to date_day fields
            if dt.year == 2025 and dt.month == 6:
                if dt.day == 10:
                    col = 'date_day1'
                elif dt.day == 11:
                    col = 'date_day2'
                elif dt.day == 12:
                    col = 'date_day3'
        except Exception:
            # If parsing fails or date is outside expected range, do not update any checkin_day
            pass

        filename = None
        if image:
            filename = f"{code_payment}_{int(datetime.utcnow().timestamp())}.jpg"
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            with open(image_path, "wb") as f:
                f.write(base64.b64decode(image))

        if col:
            if filename:
                cur.execute(
                    f"UPDATE users_delegate SET {col} = %s, image = %s WHERE id = %s",
                    (day, filename, delegate_id)
                )
            else:
                cur.execute(
                    f"UPDATE users_delegate SET {col} = %s WHERE id = %s",
                    (day, delegate_id)
                )

        # Update users table with name, job, and company
        cur.execute("""
            UPDATE users
            SET name = %s, job_title = %s, company = %s
            WHERE id = (SELECT users_id FROM users_delegate WHERE id = %s)
        """, (name, job, company, delegate_id))

        conn.commit()

        payload = {
            "name": name,
            "company": company,
            "job_title": job,
            "code_payment": code_payment,
            "day": day
        }

        # Include full image URL in response if image exists
        if filename:
            base_url = request.url_root.rstrip('/')
            upload_folder = current_app.config['UPLOAD_FOLDER'].strip('/')
            payload['image_url'] = f"{base_url}/{upload_folder}/{filename}"

        # Send simplified payload to the webhook URL asynchronously
        webhook_payload = {
            "name": name,
            "job_title": job,
            "company": company,
            "code_payment": code_payment
        }
        def send_webhook_task(url, payload):
            try:
                requests.post(url, json=payload, timeout=5)
            except Exception:
                pass

        executor.submit(send_webhook_task, link_webhook, webhook_payload)

        conn.close()
        return jsonify({"status": 1, "message": "Check-in berhasil", "data": payload})

    except Exception as e:
        current_app.logger.exception("Error in /checkin")
        return jsonify({"status": 0, "message": f"Error: {str(e)}", "data": None}), 500