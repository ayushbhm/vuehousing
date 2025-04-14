from flask import Blueprint, request, jsonify,json
from models.user import Service, User, ServiceRequest, db, Review
from flask_jwt_extended import jwt_required, get_jwt_identity
import random  
import redis 
from  redis_decorator import cache_response
customer_bp = Blueprint('customer', __name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)



@customer_bp.route('/services_available', methods=['GET'])
@cache_response(timeout=30)  
def get_services():
    services = Service.query.all()
    services_list = [{'id': service.id, 'name': service.name} for service in services]
    return jsonify(services_list)


''''
@customer_bp.route('/services_available', methods=['GET'])
def get_services():
    cache_key = 'customer:available_services'
    cached_services = redis_client.get(cache_key)
    
    if cached_services:
        return jsonify(json.loads(cached_services))

    services = Service.query.all()
    services_list = [{'id': service.id, 'name': service.name} for service in services]
    redis_client.setex(cache_key, 300, json.dumps(services_list))

    return jsonify(services_list)

'''
'''@customer_bp.route('/services_available', methods=['GET'])
def get_services():
    
    cached_services = redis_client.get('available_services')
    if cached_services:
        # If found in cache, return the cached data
        return jsonify(eval(cached_services))  # Convert string back to list of dictionaries
    
    services = Service.query.all()
    # Return a list of dictionaries containing both id and name
    return jsonify([{'id': service.id, 'name': service.name} for service in services])'''

@customer_bp.route('/service_details/<int:id>', methods=['GET'])
@cache_response(timeout=300)
def get_service_details(id):
    
    service = Service.query.get(id)  
    
    if service:
        
        services_with_same_name = Service.query.filter_by(name=service.name).all()
        
        
        service_list = []
        for s in services_with_same_name:
            service_list.append({
                'id': s.id,
                'name': s.name,
                'base_price': s.base_price,
                'time_required': s.time_required,
                'description': s.description
            })
        return jsonify(service_list) 
    else:
        
        return jsonify({'error': 'Service not found'}), 404
    
    
    
@customer_bp.route('/get_particular_service/<int:id>', methods=['GET'])
@cache_response(timeout=300)
def get_specific_service(id):
    # Query the service by ID
    service = Service.query.get(id)  # Fetch the service with the specified ID
    
    if service:
        # Return the details of the service as a JSON response
        service_details = {
            'id': service.id,
            'name': service.name,
            'base_price': service.base_price,
            'time_required': service.time_required,
            'description': service.description
        }
        return jsonify(service_details)  # Return the service details
    else:
        # Return a 404 error if the service is not found
        return jsonify({'error': 'Service not found'}), 404
    
   
@customer_bp.route('/customer_service_requests', methods=['GET'])

@jwt_required()  
def get_service_requests():
    current_user = get_jwt_identity()  # Get the current user's identity from the JWT
    current_user_id = current_user['id']  # Extract the user ID from the identity dictionary
    print(current_user_id)
    
    
    
    # Fetch service requests for the logged-in customer, joining with User and Service tables
    service_requests = (
        ServiceRequest.query
        .join(User, ServiceRequest.professional_id == User.id, isouter=True)  # Join with User for professional details
        .join(Service, ServiceRequest.service_id == Service.id)  # Join with Service for service details
        .filter(ServiceRequest.customer_id == current_user_id)  # Filter by customer ID
        .all()
    )
    
    # Prepare the response data
    requests_data = []
    for request in service_requests:
        requests_data.append({
            'id': request.id,
            'service_id': request.service_id,
            'service_name': request.service.name,  # Get service name from the joined Service table
            'professional_name': request.professional.fullname if request.professional else None,  # Get professional name
            'professional_phone': request.professional.phone if request.professional else None,  # Get professional phone number
            'date_of_request': request.date_of_request,
            'service_status': request.service_status,
            'remarks': request.remarks
        })

    return jsonify(requests_data)


@customer_bp.route('/summary', methods=['GET'])
@cache_response(timeout=300)
@jwt_required()  
def get_service_request_status_counts():
    current_user = get_jwt_identity()  # Get the current user's identity from the JWT
    current_user_id = current_user['id']  # Extract the user ID from the identity dictionary
    print(current_user_id)

    # Count the number of service requests by status for the logged-in customer
    counts = {
        'requested': ServiceRequest.query.filter_by(customer_id=current_user_id, service_status='requested').count(),
        'closed': ServiceRequest.query.filter_by(customer_id=current_user_id, service_status='closed').count(),
        'assigned': ServiceRequest.query.filter_by(customer_id=current_user_id, service_status='assigned').count()
    }

    return jsonify(counts)


@customer_bp.route('/close_service_request/<int:request_id>/close', methods=['PUT'])
@jwt_required()  
def close_service_request(request_id):
    current_user = get_jwt_identity()  # Get the current user's identity from the JWT
    current_user_id = current_user['id']  # Extract the user ID from the identity dictionary

    # Fetch the service request by ID
    service_request = ServiceRequest.query.filter_by(id=request_id, customer_id=current_user_id).first()

    if not service_request:
        return jsonify({'error': 'Service request not found or you do not have permission to close it.'}), 404

    # Update the service request status to 'closed'
    service_request.service_status = 'closed'
    db.session.commit()  # Commit the changes to the database

    return jsonify({'message': 'Service request status updated to closed successfully.'}), 200


@customer_bp.route('/book_service/<int:service_id>', methods=['POST'])
@jwt_required()  
def book_service(service_id):
    current_user = get_jwt_identity()  
    current_user_id = current_user['id']  

    #
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    
    current_user_details = User.query.get(current_user_id)
    if not current_user_details:
        return jsonify({'error': 'User not found'}), 404

    
    existing_request = ServiceRequest.query.filter_by(
        service_id=service.id,
        customer_id=current_user_id,
        service_status='requested'  
    ).first()

    if existing_request:
        return jsonify({'error': 'You have already requested this service.'}), 400

   
    professionals = User.query.filter_by(
        service_type=service.name,  
        role='professional',
        is_verified=1,
        is_blocked=0,
        pincode=current_user_details.pincode
    ).all()
    
    if not professionals:
        return jsonify({'error': 'No available professionals for this service in your area'}), 404

    
    professional = random.choice(professionals)

   
    new_request = ServiceRequest(
        service_id=service.id,
        customer_id=current_user_id,
        professional_id=professional.id,
        service_status='requested'
    )
    db.session.add(new_request)
    db.session.commit()  

    return jsonify({'message': 'Service request sent successfully.', 'request_id': new_request.id}), 201


@customer_bp.route('/submit_review/<int:request_id>', methods=['POST'])
@jwt_required()  
def submit_review(request_id):
    current_user = get_jwt_identity()  # Get the current user's identity from the JWT
    current_user_id = current_user['id']  # Extract the user ID from the identity dictionary

    # Fetch the service request by ID
    service_request = ServiceRequest.query.filter_by(id=request_id, customer_id=current_user_id).first()

    if not service_request:
        return jsonify({'error': 'Service request not found or you do not have permission to review it.'}), 404

    # Get the review data from the request
    data = request.get_json()
    rating = data.get('rating')
    comments = data.get('comments')

    # Validate the rating
    if rating is None or rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5.'}), 400

    # Create a new review
    new_review = Review(
        service_request_id=service_request.id,
        customer_id=current_user_id,
        rating=rating,
        comments=comments
    )
    db.session.add(new_review)

    # Update the service request status to 'closed'
    service_request.service_status = 'closed'

    db.session.commit()  # Commit the changes to the database

    return jsonify({'message': 'Review submitted successfully and service request closed.'}), 201




def get_user_count():
    """Fetch the count of users from the database."""
    try:
        count = User.query.count() 
        return count
    except Exception as e:
        print(f"Error fetching user count: {str(e)}")
        return 0  








