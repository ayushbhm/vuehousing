from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from celery.schedules import crontab,schedule
from flask_jwt_extended import JWTManager

from routes.auth_routes import auth_bp  
from models.user import db  
from routes.service_routes import service_bp
from routes.admin_routes import admin_bp
from routes.professional_routes import prof_bp
from routes.customer_routes import customer_bp
from tasks.email_tasks import daily_reminder,notify_professionals_of_pending_requests , send_monthly_activity_reports
import redis

from routes.email_routes import email_bp  

from config import Config 

from celery_worker import celery_init_app
app = Flask(__name__)
CORS(app)  
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'your_super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///house.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REDIS_URL'] = "redis://127.0.0.1:5000"  
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

app.config.from_object(Config)



db.init_app(app) 

 
app.register_blueprint(auth_bp, url_prefix='/auth') 
app.register_blueprint(service_bp,url_prefix='/service')
app.register_blueprint(admin_bp,url_prefix='/admin')
app.register_blueprint(prof_bp,url_prefix='/prof')
app.register_blueprint(customer_bp,url_prefix='/customer')

app.register_blueprint(email_bp, url_prefix='/email')

celery_app = celery_init_app(app)
@app.route('/')
def hello_world():
    return 'Hello, World!'
from datetime import datetime


@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    current_time = datetime.now()
    print(f"Current time (as Celery sees it): {current_time}")
    
    sender.add_periodic_task(
        
        crontab(hour=14, minute=20, day_of_month=5),
        #schedule(150),
        daily_reminder.s('narendra@email.com', 'Daily Reminder'),
    )
    
    sender.add_periodic_task(
        schedule(150),
        
        notify_professionals_of_pending_requests.s( ),
    )
    
    
    sender.add_periodic_task(
        schedule(5),
        send_monthly_activity_reports.s( ),
    )
    



if __name__ == '__main__':
    #with app.app_context():
        #db.create_all()  
    app.run(debug=True, host='0.0.0.0', port=5000)