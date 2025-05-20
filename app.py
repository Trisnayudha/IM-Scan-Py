# app.py
from flask import Flask, send_from_directory
from config import Config
from routes.scan_qr import scan_qr_bp
from routes.check_face import check_face_bp
from routes.checkin import checkin_bp
from routes.list_delegate import list_delegate_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(scan_qr_bp)
app.register_blueprint(check_face_bp)
app.register_blueprint(checkin_bp)
app.register_blueprint(list_delegate_bp)

# Route untuk serve file di folder uploads
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)