from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)

initialize_db(app)
initialize_routes(api)

SWAGGER_URL = '/api/doc'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Catalog of users'
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

app.run(host='0.0.0.0',debug=True,port='5000')