from flask import Blueprint, send_from_directory
import os

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/', defaults={'path': ''})
@frontend_bp.route('/<path:path>')
def serve_frontend(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    if path != "" and os.path.exists(os.path.join(static_folder, path)):
        return send_from_directory(static_folder, path)
    else:
        return send_from_directory(static_folder, 'index.html')