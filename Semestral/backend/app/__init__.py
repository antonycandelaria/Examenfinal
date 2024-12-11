from flask import Flask, redirect  # Asegúrate de importar `redirect` de Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

# Inicialización de las extensiones
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Crea e inicializa la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'mi_secreto_seguro'
    # Inicializa las extensiones con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Redirigir la raíz (/) a /api/
    @app.route('/')
    def index():
        return redirect('/api/')
    
    # Registro de Blueprints
    from .routes import api_bp  # Importa solo después de inicializar la app
    app.register_blueprint(api_bp, url_prefix='/api')
   
    return app

