from flask import Blueprint, request,jsonify
from models.user import Service,User,ServiceRequest, Review
from models.user import db 
from tasks.email_tasks import export_all_service_requests
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/add_service', methods=['POST'])
def add_service():
    data = request.get_json()
    if not data or 'name' not in data or 'base_price' not in data or 'time_required' not in data:
        return '', 

    new_service = Service(
        name=data['name'],
        base_price=data['base_price'],
        time_required=data['time_required'],
        description=data.get('description')
    )

    db.session.add(new_service)
    db.session.commit()

    return '', 201  

@admin_bp.route('/edit_service/<int:service_id>', methods=['PUT'])
def edit_service(service_id):
    data = request.get_json()
    if not data or 'name' not in data:
        return '', 400  

    service = Service.query.get(service_id)
    if not service:
        return '', 404  

    service.name = data['name']
    service.base_price = data.get('base_price', service.base_price)
    service.time_required = data.get('time_required', service.time_required)
    service.description = data.get('description', service.description)

    db.session.commit()

    return '', 200  


@admin_bp.route('/delete_service/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return '', 404  

    db.session.delete(service)
    db.session.commit()

    return '', 200 


@admin_bp.route('/all_services', methods=['GET'])
def get_services():
    services = Service.query.all()  
    services_list = [
        {
            'id': service.id,
            'name': service.name,
            'base_price': service.base_price,
            'time_required': service.time_required,
            'description': service.description
        }
        for service in services
    ]
    return jsonify(services_list), 200 


@admin_bp.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return '', 404  

    return '', 200 




@admin_bp.route('/get_all_professionals', methods=['GET'])
def get_all_professionals():
    professionals = User.query.filter_by(role='professional').all()  # Fetch all professionals
    professionals_list = [
        {
            'id': user.id,
            'fullname': user.fullname,
            'email': user.email,
            'phone': user.phone,
            'address': user.address,
            'pincode': user.pincode,
            'service_type': user.service_type,
            'experience': user.experience,
            'is_verified': user.is_verified,
            'is_blocked': user.is_blocked
        }
        for user in professionals
    ]
    return jsonify(professionals_list), 200  # Return the list of professionals

@admin_bp.route('/delete_professional_entry/<int:professional_id>', methods=['DELETE'])
def delete_professional_entry(professional_id):
    service = Service.query.get(professional_id)
    if not service:
        return '', 404  

    db.session.delete(service)
    db.session.commit()

    return '', 200  


@admin_bp.route('/verify_professional/<int:professional_id>', methods=['PATCH'])
def verify_professional(professional_id):
    service = Service.query.get(professional_id)
    
    if not service:
        return '', 404  

    if service.is_verified == 0:
         service.is_verified = 1# Set is_verified to 1
         db.session.commit()

    return '', 200  

@admin_bp.route('/block_professional/<int:professional_id>', methods=['POST'])
def block_professional(professional_id):
    
    professional = User.query.get(professional_id)  
    
    if not professional:
        return '', 404  

    # Check if the user is indeed a professional
    if professional.role != 'professional':
        return '', 400  

    # Toggle the is_blocked status
    professional.is_blocked = not professional.is_blocked  
    db.session.commit()  

    return '', 200  


@admin_bp.route('/toggle_professional_verification/<int:professional_id>', methods=['PATCH'])
def toggle_professional_verification(professional_id):
    professional = User.query.get(professional_id)  # Fetch the professional by ID
    if not professional:
        return '', 404  # Return 404 if the professional does not exist

    # Toggle the is_verified status
    professional.is_verified = 1 if professional.is_verified == 0 else 0
    db.session.commit()  # Commit the changes to the database

    return '', 200  # Return a success response


@admin_bp.route('/all_service_requests', methods=['GET'])
def get_all_service_requests():
    service_requests = ServiceRequest.query.all()
    service_requests_list = [
        {
            'id': request.id,
            'service_id': request.service_id,
            'service_name': request.service.name,  
            'customer_id': request.customer_id,
            'customer_name': request.customer.fullname,  
            'professional_id': request.professional_id,
            'professional_name': request.professional.fullname if request.professional else None,  
            'date_of_request': request.date_of_request,
            'date_of_completion': request.date_of_completion,
            'service_status': request.service_status,
            'remarks': request.remarks
        }
        for request in service_requests
    ]
    return jsonify(service_requests_list), 200

@admin_bp.route('/summary', methods=['GET'])
def get_summary():
    try:
        # Count total customers and professionals
        total_customers = User.query.filter_by(role='customer').count()
        total_professionals = User.query.filter_by(role='professional').count()

        # Count total service requests
        total_service_requests = ServiceRequest.query.count()

        # Count total closed requests
        total_closed_requests = ServiceRequest.query.filter_by(service_status='closed').count()

        # Count total pending requests
        total_pending_requests = ServiceRequest.query.filter(ServiceRequest.service_status.in_(['requested', 'assigned', 'accepted'])).count()

        # Create a summary dictionary
        summary = {
            'total_customers': total_customers,
            'total_professionals': total_professionals,
            'total_service_requests': total_service_requests,
            'total_closed_requests': total_closed_requests,
            'total_pending_requests': total_pending_requests
        }
        print(summary)

        return jsonify(summary), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/get_all_customers', methods=['GET'])
def get_all_customers():
    customers = User.query.filter_by(role='customer').all()  # Fetch all customers
    customers_list = [
        {
            'id': user.id,  # Include ID if needed for reference
            'fullname': user.fullname,
            'email': user.email,
            'phone': user.phone,
            'address': user.address,
            'pincode': user.pincode
        }
        for user in customers
    ]
    return jsonify(customers_list), 200  # Return the list of customers




@admin_bp.route('/all_reviews', methods=['GET'])
def get_all_reviews():
    try:
        reviews = Review.query.all()  
        reviews_list = [
            {
                'id': review.id,
                'service_request_id': review.service_request_id,
                'customer_id': review.customer_id,
                'rating': review.rating,
                'comments': review.comments
            }
            for review in reviews
        ]
        return jsonify(reviews_list), 200 
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle any errors
    
    


@admin_bp.route("/trigger_export_all")
def trigger_export_all():
    """
    API to trigger the export of all service requests.
    """
    
    task = export_all_service_requests.delay()  # Trigger the Celery task

    return jsonify({"message": "Export job triggered successfully", "task_id": task.id}), 202
