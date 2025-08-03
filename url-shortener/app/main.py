from flask import Flask, jsonify, request,redirect, abort
from app.database.db import init_db
from app.utils.routes import bp

def create_app():
    app = Flask(__name__)
    init_db()
    app.register_blueprint(bp)
    return app

app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)