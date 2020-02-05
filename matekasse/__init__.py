from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from matekasse.config import Config

db = SQLAlchemy()
socketio = SocketIO()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from matekasse.main.routes import main
    from matekasse.user.routes import user
    from matekasse.overview.routes import overview
    from matekasse.item.routes import item
    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(overview)
    app.register_blueprint(item)

    socketio.init_app(app)
    return app

