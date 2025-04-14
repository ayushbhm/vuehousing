from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User  
from models.user import db  
from werkzeug.security import generate_password_hash
auth_bp = Blueprint('auth', __name__)
from werkzeug.security import check_password_hash
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    
    user = User.query.filter_by(email=username).first()

    if user:
    
        if user.password_hash == password:
            access_token = create_access_token(identity={'id': user.id, 'role': user.role})
            return jsonify(access_token=access_token, role=user.role), 200

        
        if check_password_hash(user.password_hash, password):
            
            user.password_hash = generate_password_hash(password)
            db.session.commit()  

            access_token = create_access_token(identity={'id': user.id, 'role': user.role})
            return jsonify(access_token=access_token, role=user.role), 200

    return jsonify({"msg": "Bad username or password"}), 401


@auth_bp.route('/create_user_account', methods=['POST'])
def create_user_account():
    data = request.json
    email = data.get('email')
    fullname = data.get('username')
    password = data.get('password')
    password_hash = generate_password_hash(password)
    address = data.get('address')
    pincode = data.get('pincode')
    phone = data.get('phone')
    

    
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({"message": "Email already exists"}), 400

    
    existing_phone = User.query.filter_by(phone=phone).first()
    if existing_phone:
        return jsonify({"message": "Phone number already exists"}), 400
    
    
    new_request = User(
    fullname=fullname,
    password_hash =  password_hash,
    email = email,
    address = address,
    pincode = pincode,
    phone = phone,
    role = 'customer'
    
    )
    try:
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message' : 'registered successfully'}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@auth_bp.route('/create_professional_account', methods=['POST'])
def create_professional_account():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    fullname = data.get('fullname')
    
    # New field for full name
    service_name = data.get('service_name')  # New field for service name
    experience = data.get('experience')  # New field for experience
    address = data.get('address')
    phone  = data.get('phone')
    pincode = data.get('pincode')
    password_hash = generate_password_hash(password)



    # Check for existing email
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({"message": "Email already exists"}), 400

    # Check for existing phone number (if applicable)
    existing_phone = User.query.filter_by(phone=data.get('phone')).first()
    if existing_phone:
        return jsonify({"message": "Phone number already exists"}), 400

    # Create a new User instance for the professional
    new_professional = User(
        fullname=fullname,
        password_hash=password_hash,
        email=email,
        address=address,
        pincode=pincode,
        phone=phone,  # Assuming phone is passed in the request
        role='professional',  # Set role to 'professional'
        service_type=service_name,  # Assuming service_type is the same as service_name
        experience=experience  # Set experience
    )

    try:
        db.session.add(new_professional)
        db.session.commit()
        return jsonify({'message': 'Professional registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


