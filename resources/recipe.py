from flask import request
from http import HTTPStatus
from flask_restful import Resource
import psycopg2

# Connect to the Postgres database
conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_username",
    password="your_password"
)

class RecipeListResource(Resource):
    def get(self):
        # Fetch recipes from the Postgres database
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM recipes WHERE is_publish = TRUE")
            recipes = cur.fetchall()

        data = []
        for recipe in recipes:
            data.append({
                'id': recipe[0],
                'name': recipe[1],
                'description': recipe[2],
                'num_of_servings': recipe[3],
                'cook_time': recipe[4],
                'directions': recipe[5]
            })

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        # Insert the new recipe into the Postgres database
        with conn.cursor() as cur:
            cur.execute("INSERT INTO recipes (name, description, num_of_servings, cook_time, directions, is_publish) VALUES (%s, %s, %s, %s, %s, %s)",
                        (data['name'], data['description'], data['num_of_servings'], data['cook_time'], data['directions'], True))
        conn.commit()

        # Retrieve the newly inserted recipe
        recipe_id = cur.lastrowid
        recipe = {
            'id': recipe_id,
            'name': data['name'],
            'description': data['description'],
            'num_of_servings': data['num_of_servings'],
            'cook_time': data['cook_time'],
            'directions': data['directions']
        }

        return recipe, HTTPStatus.CREATED

class RecipeResource(Resource):
    def get(self, recipe_id):
        # Fetch the recipe from the Postgres database
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM recipes WHERE id = %s AND is_publish = TRUE", (recipe_id,))
            recipe = cur.fetchone()

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        return {
            'id': recipe[0],
            'name': recipe[1],
            'description': recipe[2],
            'num_of_servings': recipe[3],
            'cook_time': recipe[4],
            'directions': recipe[5]
        }, HTTPStatus.OK

    def put(self, recipe_id):
        data = request.get_json()

        # Update the recipe in the Postgres database
        with conn.cursor() as cur:
            cur.execute("UPDATE recipes SET name = %s, description = %s, num_of_servings = %s, cook_time = %s, directions = %s WHERE id = %s",
                        (data['name'], data['description'], data['num_of_servings'], data['cook_time'], data['directions'], recipe_id))
        conn.commit()

        return {
            'id': recipe_id,
            'name': data['name'],
            'description': data['description'],
            'num_of_servings': data['num_of_servings'],
            'cook_time': data['cook_time'],
            'directions': data['directions']
        }, HTTPStatus.OK

    def delete(self, recipe_id):
        # Mark the recipe as unpublished in the Postgres database
        with conn.cursor() as cur:
            cur.execute("UPDATE recipes SET is_publish = FALSE WHERE id = %s", (recipe_id,))
        conn.commit()

        return {}, HTTPStatus.NO_CONTENT

class RecipePublishResource(Resource):
    def patch(self, recipe_id):
        # Publish the recipe in the Postgres database
        with conn.cursor() as cur:
            cur.execute("UPDATE recipes SET is_publish = TRUE WHERE id = %s", (recipe_id,))
        conn.commit()

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, recipe_id):
        # Unpublish the recipe in the Postgres database
        with conn.cursor() as cur:
            cur.execute("UPDATE recipes SET is_publish = FALSE WHERE id = %s", (recipe_id,))
        conn.commit()

        return {}, HTTPStatus.NO_CONTENT
