# Simple-Python-App
Data Querying Mechanism with FastAPI, Pydantic, and SQLAlchemy

This project implements a FastAPI-based backend with models for posts, comments, tags, and users, alongside several reusable and extendable API endpoints.

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
-> git clone <repository-url>  
-> cd <project-directory>  
Install dependencies:  
-> pip install -r requirements.txt  
Run the server:  
-> uvicorn app.main:app --reload  
