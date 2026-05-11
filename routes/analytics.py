from flask import Blueprint, jsonify
from analytics.task_analytics import generate_task_analytics

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
def analytics():

    data = generate_task_analytics()

    return jsonify(data)