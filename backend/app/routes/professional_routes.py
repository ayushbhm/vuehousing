from flask import Blueprint, jsonify, request
from models.user import ServiceRequest, User, Review
from models.user import db
from flask_jwt_extended import jwt_required, get_jwt_identity  # Import JWT functions
from datetime import datetime

prof_bp = Blueprint('prof', __name__)


@prof_bp.route('/upcoming_service_requests', methods=['GET'])
@jwt_required()  # Protect the route with JWT authentication
def get_upcoming_service_requests():
    # Get the identity from the JWT token
    identity = get_jwt_identity()  # This should return the identity (could be a dict)

    # Extract the professional ID from the identity
    current_professional_id = identity['id'] if isinstance(identity, dict) else identity

    # Print the professional ID to the terminal for verification
    print(f"Current Professional ID: {current_professional_id}")

    # Fetch upcoming service requests for the logged-in professional
    upcoming_requests = ServiceRequest.query.join(User, ServiceRequest.customer_id == User.id).filter(
        ServiceRequest.professional_id == current_professional_id,
        ServiceRequest.service_status == 'requested'  # Assuming 'requested' indicates upcoming
    ).all()

    # Prepare the response data
    requests_list = [
        {
            'id': request.id,
            'customer_name': request.customer.fullname,  # Get customer name
            'customer_phone': request.customer.phone,     # Get customer phone
            'customer_pincode': request.customer.pincode,  # Get customer pincode
            'date_of_request': request.date_of_request,
            'service_status': request.service_status,
            'remarks': request.remarks
        }
        for request in upcoming_requests
    ]

    print(requests_list)

    return jsonify(requests_list), 200  # Return the list of upcoming service requests



@prof_bp.route('/closed_service_requests', methods=['GET'])
@jwt_required()  # Protect the route with JWT authentication
def get_closed_service_requests():
    # Get the identity from the JWT token
    identity = get_jwt_identity()  # This should return the identity (could be a dict)

    # Extract the professional ID from the identity
    current_professional_id = identity['id'] if isinstance(identity, dict) else identity

    # Print the professional ID to the terminal for verification
    print(f"Current Professional ID: {current_professional_id}")

    # Fetch closed service requests for the logged-in professional
    closed_requests = ServiceRequest.query.join(User, ServiceRequest.customer_id == User.id).filter(
        ServiceRequest.professional_id == current_professional_id,
        ServiceRequest.service_status == 'closed' or ServiceRequest.service_status == 'rejected'   # Assuming 'closed' indicates completed requests
    ).all()

    # Prepare the response data
    requests_list = [
        {
            'id': request.id,
            'customer_name': request.customer.fullname,  # Get customer name
            'customer_phone': request.customer.phone,     # Get customer phone
            'customer_pincode': request.customer.pincode,  # Get customer pincode
            'date_of_completion': request.date_of_completion,  # Date of completion
            'remarks': request.remarks,  # Remarks
            'service_status': request.service_status  # Status of the service request
        }
        for request in closed_requests
    ]
    
    print(requests_list)

    return jsonify(requests_list), 200  # Return the list of closed service requests


@prof_bp.route('/service_request/<int:request_id>/accept', methods=['POST'])
@jwt_required()  # Protect the route with JWT authentication
def accept_service_request(request_id):
    # Get the identity from the JWT token
    identity = get_jwt_identity()
    current_professional_id = identity['id'] if isinstance(identity, dict) else identity

    # Fetch the service request
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"message": "Service request not found."}), 404

    # Check if the request is already accepted or rejected
    if service_request.service_status in ['accepted', 'rejected']:
        return jsonify({"message": "Service request has already been accepted or rejected."}), 400

    # Update the service request status
    service_request.professional_id = current_professional_id
    service_request.service_status = 'assigned'  # Mark as accepted
    db.session.commit()

    return jsonify({"message": "Service request accepted."}), 200


@prof_bp.route('/service_request/<int:request_id>/reject', methods=['POST'])
@jwt_required()  # Protect the route with JWT authentication
def reject_service_request(request_id):
    # Get the identity from the JWT token
    identity = get_jwt_identity()
    current_professional_id = identity['id'] if isinstance(identity, dict) else identity

    # Fetch the service request
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"message": "Service request not found."}), 404

    # Check if the request is already accepted or rejected
    if service_request.service_status in ['accepted', 'rejected']:
        return jsonify({"message": "Service request has already been accepted or rejected."}), 400

    # Update the service request status
    service_request.service_status = 'rejected'  # Mark as rejected
    db.session.commit()

    return jsonify({"message": "Service request rejected."}), 200


@prof_bp.route('/accepted_service_requests', methods=['GET'])
@jwt_required()  # Protect the route with JWT authentication
def get_accepted_service_requests():
    # Get the identity from the JWT token
    identity = get_jwt_identity()  # This should return the identity (could be a dict)

    # Extract the professional ID from the identity
    current_professional_id = identity['id'] if isinstance(identity, dict) else identity

    # Fetch accepted service requests for the logged-in professional
    accepted_requests = ServiceRequest.query.join(User, ServiceRequest.customer_id == User.id).filter(
        ServiceRequest.professional_id == current_professional_id,
        ServiceRequest.service_status == 'assigned'  # Filter for accepted requests
    ).all()

    # Prepare the response data
    requests_list = [
        {
            'id': request.id,
            'customer_name': request.customer.fullname,  # Get customer name
            'customer_phone': request.customer.phone,     # Get customer phone
            'customer_pincode': request.customer.pincode,  # Get customer pincode
            'date_of_request': request.date_of_request,    # Date of request
            
            'service_status': request.service_status  # Status of the service request
        }
        for request in accepted_requests
    ]

    return jsonify(requests_list), 200  # Return the list of accepted service requests


@prof_bp.route('/professional_stats', methods=['GET'])
@jwt_required()  # Protect the route with JWT authentication
def get_professional_stats():
    # Get the identity from the JWT token
    identity = get_jwt_identity()  # This should return the identity (could be a dict)

    # Extract the professional ID from the identity
    current_professional_id = identity['id'] if isinstance(identity, dict) else identity

    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Total service requests received
    total_requests_received = ServiceRequest.query.filter(
        ServiceRequest.professional_id == current_professional_id
    ).count()

    # Total closed requests
    total_closed_requests = ServiceRequest.query.filter(
        ServiceRequest.professional_id == current_professional_id,
        ServiceRequest.service_status == 'closed'
    ).count()

    # Total rejected requests
    total_rejected_requests = ServiceRequest.query.filter(
        ServiceRequest.professional_id == current_professional_id,
        ServiceRequest.service_status == 'rejected'
    ).count()

    # Requests received this month
    requests_this_month = ServiceRequest.query.filter(
        ServiceRequest.professional_id == current_professional_id,
        db.extract('month', ServiceRequest.date_of_request) == current_month,
        db.extract('year', ServiceRequest.date_of_request) == current_year
    ).count()

    # Closed requests this month
    closed_requests_this_month = ServiceRequest.query.filter(
        ServiceRequest.professional_id == current_professional_id,
        ServiceRequest.service_status == 'closed',
        db.extract('month', ServiceRequest.date_of_completion) == current_month,
        db.extract('year', ServiceRequest.date_of_completion) == current_year
    ).count()

    # Rejected requests this month
    rejected_requests_this_month = ServiceRequest.query.filter(
        ServiceRequest.professional_id == current_professional_id,
        ServiceRequest.service_status == 'rejected',
        db.extract('month', ServiceRequest.date_of_request) == current_month,
        db.extract('year', ServiceRequest.date_of_request) == current_year
    ).count()

    # Total remarks given
    total_remarks_given = Review.query.filter(
        Review.service_request.has(professional_id=current_professional_id)
    ).count()

    # Prepare the summary data
    stats_data = {
        'total_requests_received': total_requests_received,
        'total_closed_requests': total_closed_requests,
        'total_rejected_requests': total_rejected_requests,
        'requests_this_month': requests_this_month,
        'closed_requests_this_month': closed_requests_this_month,
        'rejected_requests_this_month': rejected_requests_this_month,
        'total_remarks_given': total_remarks_given,
    }
    print(stats_data)

    return jsonify(stats_data), 200  # Return the stats data


@prof_bp.route('/profile_details', methods=['GET'])
@jwt_required()  # Protect the route with JWT authentication
def get_professional_details():
    # Get the identity of the current user (professional)
    identity = get_jwt_identity()  # This should return the identity (could be a dict)

    # Extract the professional ID from the identity
    current_professional_id = identity['id'] if isinstance(identity, dict) else identity

    # Print the user ID for debugging
    print(f"Current User ID: {current_professional_id}")

    # Fetch the professional details from the database
    professional = User.query.get(current_professional_id)

    if not professional:
        return jsonify({'msg': 'Professional not found'}), 404

    # Prepare the response data
    professional_data = {
        'id': professional.id,
        'fullname': professional.fullname,
        'email': professional.email,
        'phone': professional.phone,
        'address': professional.address,
        'pincode': professional.pincode,
        'service_type': professional.service_type,
        'experience': professional.experience,
        'is_verified': professional.is_verified,
        'is_blocked': professional.is_blocked,
    }

    return jsonify(professional_data), 200


@prof_bp.route('/update_profile', methods=['POST'])  # Use POST for updating
@jwt_required()  # Protect the route with JWT authentication
def update_professional_details():
    # Get the identity of the current user (professional)
    identity = get_jwt_identity()  # This will return the identity
    current_professional_id = identity['id'] if isinstance(identity, dict) else identity  # Extract ID

    # Fetch the professional details from the database
    professional = User.query.get(current_professional_id)

    if not professional:
        return jsonify({'msg': 'Professional not found'}), 404

    # Get the data from the request
    data = request.get_json()

    # Update the fields that are allowed to be changed
    if 'fullname' in data:
        professional.fullname = data['fullname']
    if 'email' in data:
        professional.email = data['email']
    if 'phone' in data:
        professional.phone = data['phone']
    if 'address' in data:
        professional.address = data['address']
    if 'pincode' in data:
        professional.pincode = data['pincode']
    if 'service_type' in data:
        professional.service_type = data['service_type']
    if 'experience' in data:
        professional.experience = data['experience']

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'msg': 'Professional details updated successfully.'}), 200








