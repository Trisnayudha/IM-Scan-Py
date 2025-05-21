from flask import Blueprint, jsonify

check_face_bp = Blueprint('check_face', __name__)

@check_face_bp.route('/check-face', methods=['GET','POST'])
def check_face():
    return jsonify({
        "status": 0,
        "message": "Fitur face detection sudah dihapus.",
        "data": None
    })