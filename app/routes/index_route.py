from flask import Blueprint, request, jsonify, render_template

index_bp = Blueprint('menu', __name__)

@index_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')