from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os

db = SQLAlchemy()
DB_NAME = "journal_app"  # Changed from "database" to avoid reserved word

def createapp():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "hey there!"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Create database first, before initializing SQLAlchemy
    if not create_database_if_not_exists():
        print("Failed to create database. Exiting...")
        return None
    
    localhost_name = os.getenv("LOCALHOST")
    password_name = os.getenv("PASSWORD")
    root_name = os.getenv("ROOT")
    
    # Now set the database URI and initialize SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{root_name}:{password_name}@{localhost_name}/{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    # Create tables
    try:
        with app.app_context():
            db.create_all()
            print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        return None

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database_if_not_exists():
    """Create MySQL database if it doesn't exist"""
    try:
        # Connect to MySQL server using PyMySQL (without specifying database)
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="password"
        )
        
        cursor = connection.cursor()
        
        # Check if database exists (using backticks to escape database name)
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if DB_NAME not in databases:
            # Use backticks to escape the database name in case it's a reserved word
            cursor.execute(f"CREATE DATABASE `{DB_NAME}`")
            print(f"Database '{DB_NAME}' created successfully")
        else:
            print(f"Database '{DB_NAME}' already exists")
            
        cursor.close()
        connection.close()
        return True
            
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def create_database(app):
    """Create MySQL database if it doesn't exist, then create tables"""
    try:
        # Connect to MySQL server using PyMySQL (without specifying database)
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="password"
        )
        
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if DB_NAME not in databases:
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database '{DB_NAME}' created successfully")
        else:
            print(f"Database '{DB_NAME}' already exists")
            
        cursor.close()
        connection.close()
        
        # Now create tables using SQLAlchemy
        with app.app_context():
            db.create_all()
            print("Database tables created successfully")
            
    except Exception as e:
        print(f"Error creating database: {e}")