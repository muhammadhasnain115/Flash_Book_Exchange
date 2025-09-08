from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # blueprints (inside the function)
    from app.auth.routes import auth_bp
    from app.books.routes import books_bp
    from app.donations.routes import donations_bp
    from app.main.routes import main_bp
    from app.account.routes import bp as account_bp
    
    app.register_blueprint(account_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(donations_bp, url_prefix="/donate")
    app.register_blueprint(main_bp)

    # create instance folder and DB if not exists
    import os
    os.makedirs(app.instance_path, exist_ok=True)

    return app
