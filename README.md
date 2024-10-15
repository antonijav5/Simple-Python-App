# Simple-Python-App
Data Querying Mechanism with FastAPI, Pydantic, and SQLAlchemy

This project implements a FastAPI-based backend with models for posts, comments, tags, and users, alongside several reusable and extendable API endpoints.

## Features

- Create, retrieve, and manage users, posts, comments, and tags.
- Populate the database with sample data for testing.
- Implemented unit tests using `pytest` to ensure the functionality of the API endpoints.

# Models and Relationships
1. Post
  Belongs to a User  
  Has many Comments  
  Has many Tags

3. Comment  
  Belongs to a Post  
  Belongs to a User

5. Tag  
  Has many Posts

7. User  
  Has many Comments  
  Has many Posts

# API Endpoints  
GET /api/posts?status=draft&include=tags,user  
-> Fetch posts filtered by the specified status (draft).  
-> Include related tags and user information in the response.  

GET /api/posts/{id}?include=tags,user,comments  
-> Retrieve a specific post by its ID.  
-> Include associated tags, user, and comments in the response.  

GET /api/users/{id}?include=posts,comments  
-> Retrieve a specific user by their ID.  
-> Include related posts and comments in the response.  

Reusability and Extensibility
The querying mechanism has been designed to be highly reusable and extensible. A generic query function, generic_query(), has been implemented to allow the flexible filtering and inclusion of related data for any model.

# Key features for reusability:  
-> Filters: You can dynamically apply filters to the query based on model attributes. For example, filtering posts by status.  
-> Includes: You can easily include related models (such as tags, users, or comments) by passing them to the includes parameter.  
-> Generic for Multiple Models: The generic_query() function can be used across different models like Post, User, Tag, etc., making it adaptable to future needs without duplicating code.  
This design allows the querying logic to be extended easily by adding new models or relationships without the need to rewrite or modify existing code.  

# Setup and Installation  
Clone the repository:  
-> git clone [<repository-url>  ](https://github.com/antonijav5/Simple-Python-App.git)
-> relocate to Simple-Python-App folder 
Install dependencies:  
-> pip install -r requirements.txt  
Run the server:  
-> uvicorn app.main:app --reload  

# Testing  
This project includes unit tests for the FastAPI application using pytest. The tests are located in the tests directory.  
-> Test Structure  
test_app: A fixture that sets up a FastAPI test client for making requests to the application during testing.  
db_session: A fixture that manages the database session. It drops all tables, creates new ones, and populates the database with sample data before running the tests.  
Tests: There are multiple test functions to verify the correctness of the API endpoints:  
test_get_posts: Tests fetching posts with a specific status.  
test_get_post: Tests fetching a single post by its ID.  
test_get_user: Tests fetching a user by their ID.  
-> Running Tests  
To run the tests, use the following command:  
pytest  
OR  
pytest -W ignore::DeprecationWarning   

