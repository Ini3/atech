import os
from flask import request, abort, Blueprint, send_from_directory

swagger = Blueprint('swagger', __name__, url_prefix='/docs')

@swagger.route('/')
def swagger_ui():
    return send_from_directory('static/swagger', 'index.html')

@swagger.route('/openapi.json')
def swagger_spec():
    return send_from_directory('static/swagger', 'openapi.json')


API_KEY = os.environ.get('ADMIN_API_KEY')

def require_api_key():
    if request.headers.get('X-API-KEY') != API_KEY:
        abort(401)