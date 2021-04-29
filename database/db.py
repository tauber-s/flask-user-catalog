from flask_sqlalchemy import SQLAlchemy
import redis

db_psql = SQLAlchemy()
db_redis = redis.Redis(
    host='redis-cont', 
    port=6379, 
    password='psw231377',
    socket_timeout=5,
    decode_responses=True)

def initialize_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@postgresql/postgres'
    db_psql.init_app(app)
    with app.app_context():
        db_psql.create_all()
