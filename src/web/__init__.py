from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Importamos y registramos las rutas (el controlador)
    from src.web.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app