from flask import Blueprint, jsonify
from models.user import Service

service_bp = Blueprint('service', __name__)

@service_bp.route('/professional_services', methods=['GET'])
def get_services():
    """
    API to fetch unique professional services.
    """
    # Fetch unique service names from the database
    services = Service.query.distinct(Service.name).all()

    # Prepare the list of services
    service_list = [{'id': service.id, 'name': service.name} for service in services]

    return jsonify(service_list), 200


