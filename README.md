# Full Stack Nanodegree Capstone - Course Catalog API

The Course Catalog API allows training centres to handle courses and the projects for each of them.

This project is built as Capstone for the Full Stack Nanodegree at Udacity and it does not include a frontend. Endpoints can be called using tools like curl or postman. Examples for all of them are included in the postman collection file in this repository.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql myapp < capstone.psql
```

## Environment Variable Setup
The environment variables can be modified in setup.sh.

## Running the server

First ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source setup.sh
export FLASK_ENV=development (optional for development)
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

## Testing
To run the tests, run
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.psql
python test_app.py
```

Note: You will also need to set valid access tokens in setup.sh

## API Documentation

### Base URL
The API can be accessed [here](https://fsnd-capstone-api.herokuapp.com/courses)

### Roles and permissions

- Public: Has no specific permissions. Can fetch the list of courses and projects

- Instructor: Can create, update and delete projects

- Program Manager: All permissions from Instructors plus can create, update and delete courses


### List of endpoints

[GET '/courses?page={page_number}'](#get_courses)

[POST '/courses'](#post_courses)

[PATCH '/courses/{id}'](#patch_courses)

[DELETE '/courses/{id}'](#delete_courses)

[GET '/projects?page={page_number}'](#get_projects)

[POST '/projects'](#post_projects)

[PATCH '/projects/{id}'](#patch_projects)

[DELETE '/queprojectsstions/{id}'](#delete_projects)

### Endpoints details

<a name="get_courses"></a>GET '/courses?page={page_number}'
- Fetches the list of courses
- Request Arguments: page_number (optional, default = 1)
- Returns: An object with a success key that contains a boolean and a courses key, that contains the list of courses. 
```
{
  "courses": [
    {
      "description": "Become a Full Stack Developer with this course",
      "id": 3,
      "name": "Full Stack",
      "price": 249
    },
    {
      "description": "Become a Full Stack Developer with this course",
      "id": 1,
      "name": "Full Stack",
      "price": 239
    }
  ],
  "success": true
}
```

<a name="post_courses"></a>POST '/courses'
- Creates a new course
- Requires permissions: post:courses
- Request Arguments: An object with the course name, description and price
```
{
    "name": "Full Stack",
    "description": "Become a Full Stack Developer with this course",
    "price": 249
}
```
- Returns: An object with the sucess result and the new course
```
{
  "courses": [
    {
      "description": "Become a Full Stack Developer with this course",
      "id": 4,
      "name": "Full Stack",
      "price": 249
    }
  ],
  "success": true
}
```

<a name="patch_courses"></a>PATCH '/courses/{id}'
- Updates a course
- Requires permissions: patch:courses
- Request Arguments: The id of the course and an object with the fields to update
```
{
    "price": 239
}
```
- Returns: An object with the sucess result and the updated course
```
{
  "courses": [
    {
      "description": "Become a Full Stack Developer with this course",
      "id": 1,
      "name": "Full Stack",
      "price": 239
    }
  ],
  "success": true
}
```

<a name="delete_courses"></a>DELETE '/courses/{id}'
- Deletes a course
- Requires permissions: delete:courses
- Request Arguments: The id of the course to delete
- Returns: An object with the sucess result and the id of the deleted course
```
{
  "delete": "2",
  "success": true
}
```

<a name="get_projects"></a>GET '/projects?page={page_number}'
- Fetches the list of projects
- Request Arguments: page_number (optional, default = 1)
- Returns: An object with a success key that contains a boolean and a projects key, that contains the list of projects. 
```
{
  "projects": [
    {
      "course_id": 1,
      "id": 3,
      "instructions": "Build your own project using all you have learned during the course",
      "title": "Capstone"
    }
  ],
  "success": true
}
```

<a name="post_projects"></a>POST '/projects'
- Creates a new project
- Requires permissions: post:projects
- Request Arguments: An object with the project title, instructions and course id
```
{
    "title": "Capstone",
    "instructions": "Build your own project using all you have learned during the course",
    "course_id": 1
}
```
- Returns: An object with the sucess result and the new project
```
{
  "projects": [
    {
      "course_id": 1,
      "id": 5,
      "instructions": "Build your own project using all you have learned during the course",
      "title": "Capstone"
    }
  ],
  "success": true
}
```

<a name="patch_projects"></a>PATCH '/projects/{id}'
- Updates a project
- Requires permissions: patch:projects
- Request Arguments: The id of the project and an object with the fields to update
```
{
    "title": "Full Stack Capstone"
}
```
- Returns: An object with the sucess result and the updated course
```
{
  "projects": [
    {
      "course_id": 1,
      "id": 1,
      "instructions": "Build your own project using all you have learned during the course",
      "title": "Full Stack Capstone"
    }
  ],
  "success": true
}
```

<a name="delete_projects"></a>DELETE '/projects/{id}'
- Deletes a project
- Requires permissions: delete:projects
- Request Arguments: The id of the project to delete
- Returns: An object with the sucess result and the id of the deleted projects
```
{
  "delete": "1",
  "success": true
}
```


