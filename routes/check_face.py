# routes/check_face.py
from flask import Blueprint, request, jsonify
from deepface import DeepFace
from PIL import Image
import os
from config import Config

check_face_bp = Blueprint('check_face', __name__)

@check_face_bp.route('/check-face', methods=['POST'])
def check_face():
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({"status": 0, "message": "No image uploaded", "data": None})
    try:
        img = Image.open(image_file.stream)
        tmp_path = os.path.join(Config.UPLOAD_FOLDER, 'tmp_face.jpg')
        img.save(tmp_path)
        DeepFace.analyze(img_path=tmp_path, actions=['emotion'], enforce_detection=True)
        return jsonify({"status": 1, "message": "Face detected", "data": {"face_detected": True}})
    except Exception as e:
        return jsonify({"status": 0, "message": f"No face detected: {str(e)}", "data": {"face_detected": False}})
