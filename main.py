from flask import Flask
from flask_restful import Api

from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource

import psycopg2
import os
conn = psycopg2.connect(os.environ['DATABASE_URL'])

# Connect to the Postgres database
conn = psycopg2.connect(
    host="ep-flat-resonance-a5ob2cpg.us-east-2.aws.neon.tech",
    database="neondb",
    user="neondb_owner",
    password="nID8gyVrCMQ5"
)



app = Flask(__name__)
api = Api(app)

api.add_resource(RecipeListResource, '/recipes')
api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')



if __name__ == '__main__':
    app.run(port=5000, debug=True)