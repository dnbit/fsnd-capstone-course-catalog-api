import os
from flask import Flask, request, jsonify, abort
from models import setup_db, Course, Project
from flask_cors import CORS
from auth import AuthError, requires_auth
import json

ITEMS_PER_PAGE = 10


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    def paginate_items(items, page):
        end = page * ITEMS_PER_PAGE
        start = end - ITEMS_PER_PAGE
        return items[start:end]

    # Courses
    @app.route('/courses', methods=['GET'])
    def get_courses():
        result = {
            "success": True,
        }

        page = request.args.get('page', 1, type=int)

        courses = Course.query.all()

        paginated_courses = paginate_items(courses, page)

        if not paginated_courses:
            abort(404)

        try:
            formatted_courses = [course.format() for course
                                 in paginated_courses]
            result['courses'] = formatted_courses
        except Exception as e:
            print(e)
            abort(500)

        return jsonify(result)

    @app.route('/courses', methods=['POST'])
    @requires_auth(permission='post:courses')
    def create_new_course(payload):
        courses = []
        result = {
            "success": True,
        }

        try:
            body = json.loads(request.data)

            name = body['name']
            description = body['description']
            price = body['price']

            new_course = Course(name=name, description=description,
                                price=price)
            new_course.insert()

            courses.append(new_course.format())

        except Exception as e:
            print(e)
            abort(500)

        result['courses'] = courses

        return jsonify(result)

    @app.route('/courses/<id>', methods=['PATCH'])
    @requires_auth(permission='patch:courses')
    def update_course(payload, id):
        courses = []
        result = {
            "success": True,
        }

        course = Course.query.filter(Course.id == id).one_or_none()
        if not course:
            abort(404)

        try:
            body = json.loads(request.data)

            name = body.get('name')
            description = body.get('description')
            price = body.get('price')

            if name:
                course.name = name

            if description:
                course.description = description

            if price:
                course.price = price

            courses.append(course.format())

            course.update()

        except Exception as e:
            print(e)
            abort(500)

        result['courses'] = courses

        return jsonify(result)

    @app.route('/courses/<id>', methods=['DELETE'])
    @requires_auth(permission='delete:courses')
    def delete_course(payload, id):
        result = {
            "success": True,
            'delete': id
        }

        course = Course.query.filter(Course.id == id).one_or_none()
        if not course:
            abort(404)

        try:
            course.delete()
        except Exception as e:
            print(e)
            abort(500)

        return jsonify(result)

    @app.route('/projects', methods=['GET'])
    def get_projects():
        result = {
            "success": True,
        }

        page = request.args.get('page', 1, type=int)

        projects = Project.query.all()

        paginated_projects = paginate_items(projects, page)

        if not paginated_projects:
            abort(404)

        try:
            formatted_projects = [project.format() for project
                                  in paginated_projects]
            result['projects'] = formatted_projects
        except Exception as e:
            print(e)
            abort(500)

        return jsonify(result)

    @app.route('/projects', methods=['POST'])
    @requires_auth(permission='post:projects')
    def create_new_project(payload):
        projects = []
        result = {
            "success": True,
        }

        try:
            body = json.loads(request.data)

            title = body['title']
            instructions = body['instructions']
            course_id = body['course_id']

            new_project = Project(title=title, instructions=instructions,
                                  course_id=course_id)
            new_project.insert()

            projects.append(new_project.format())

        except Exception as e:
            print(e)
            abort(500)

        result['projects'] = projects

        return jsonify(result)

    @app.route('/projects/<id>', methods=['PATCH'])
    @requires_auth(permission='patch:projects')
    def update_project(payload, id):
        projects = []
        result = {
            "success": True,
        }

        project = Project.query.filter(Project.id == id).one_or_none()
        if not project:
            abort(404)

        try:
            body = json.loads(request.data)

            title = body.get('title')
            instructions = body.get('instructions')
            course_id = body.get('course_id')

            if title:
                project.title = title

            if instructions:
                project.instructions = instructions

            if course_id:
                project.course_id = course_id

            projects.append(project.format())

            project.update()

        except Exception as e:
            print(e)
            abort(500)

        result['projects'] = projects

        return jsonify(result)

    @app.route('/projects/<id>', methods=['DELETE'])
    @requires_auth(permission='delete:projects')
    def delete_project(payload, id):
        result = {
            "success": True,
            'delete': id
        }

        project = Project.query.filter(Project.id == id).one_or_none()
        if not project:
            abort(404)

        try:
            project.delete()
        except Exception as e:
            print(e)
            abort(500)

        return jsonify(result)

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
