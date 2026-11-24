# from fastapi import FastAPI, Depends
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from database import get_db, Base, engine
# import models
# app=FastAPI()
# Base.metadata.create_all(bind=engine)
# todos=[]
# class Todo(BaseModel):
#     id:int 
#     title:str
#     completed: bool

# @app.post("/todos")
# def create_todo(todo:Todo):
#     todos.append(todo)
#     return{
#         "messege":"todo added","data":todo
#     }

# @app.get("/todos")
# def get_todo():
#     return todos

# @app.get("/todos/{todo_id}")
# def get_todos_byid(todo_id:int):
#     for todo in todos:
#         if todo.id==todo_id:
#             return todo
#     return{"error":"todo not found"}

# @app.put("/todos/{todo_id}")
# def update_todo(todo_id:int,updated_todo:Todo):
#     for index,todo in enumerate(todos):
#         if todo.id==todo_id:
#             todos[index]=updated_todo
#             return{
#                 "messege":"data updated",
#                 "data":updated_todo
#             }
#     return{"error":"todo not found"}
  
# @app.delete("/todos/{todo_id}")
# def delete_todo(todo_id:int):
#     for index,todo in enumerate(todos):
#         if todo.id==todo_id:
#             todos.pop(index)
#             return{
#                 "messege":"data deleted",
#             }
#     return{"error":"todo not found"}
# @app.get("/db-test")
# def db_test(db: Session = Depends(get_db)):
#     return{
#         "messege":"database session recived successfully"
#     }
# # class User(BaseModel):
# #     name:str
# #     age:int
# # #default paramter
# # @app.get("/products")
# # def get_products(limit:int=10):
# #     return{"limit":limit}
# # @app.get("/items")
# # def items(name:str=None,price:int=0):
# #     return{
# #         "name":name,
# #         "price":price
# #         }
# # @app.post("/create-user")
# # def create_user(user:User):
# #     return{
# #        "messege":"user craeted",
# #        "data":user
# #     }
# #query parameter
# # @app.get("/users")
# # def get_users(name):
# #     return{"name":name}
# # @app.get("/users/{user_id}")
# # def get_user(user_id:int):
# #     return{"user_id": user_id}
# # @app.get("/")
# # def home():
# #     return{"messege":"hello"}
# # #about
# # @app.get("/about")
# # def about():
# #     return{"messege":"this is about"}
# #users
# # @app.get("/user")
# # def user():
# #     return{
# #         "messege":["sushovan","dilip","pradip"]
# #            }
    






# ============================================================
# 1. IMPORTS
# ============================================================

# Import the FastAPI class to create our backend application.
# Import Depends to inject dependencies such as a database session.
# Import HTTPException to return HTTP errors such as 404 Not Found.
from fastapi import FastAPI, Depends, HTTPException

# Import BaseModel from Pydantic.
# BaseModel helps validate the data received from API requests.
from pydantic import BaseModel

# Import Session from SQLAlchemy.
# Session represents a connection/session used to communicate with the database.
from sqlalchemy.orm import Session

# Import get_db to provide a database session.
# Import Base to access SQLAlchemy model metadata.
# Import engine to connect SQLAlchemy with MySQL.
from database import get_db, Base, engine

# Import models.py, which contains our SQLAlchemy database models.
import models


# ============================================================
# 2. CREATE FASTAPI APPLICATION
# ============================================================

# Create an instance of the FastAPI application.
# The app object is used to define all our API endpoints.
app = FastAPI()


# ============================================================
# 3. CREATE DATABASE TABLES
# ============================================================

# Base.metadata contains information about our SQLAlchemy models.
# create_all() checks whether the required tables exist.
# If a table does not exist, SQLAlchemy creates it.
# bind=engine connects this operation to our MySQL database.
# Existing tables and their records are not recreated or deleted.
Base.metadata.create_all(bind=engine)


# ============================================================
# 4. PYDANTIC MODEL FOR CREATING TODOS
# ============================================================

# Create a Pydantic model named TodoCreate.
# This model validates the data received when creating a Todo.
class TodoCreate(BaseModel):

    # title must contain string data.
    # This field is required when creating a Todo.
    title: str

    # completed must contain Boolean data (True or False).
    # If the user does not provide this field, its default value is False.
    completed: bool = False


# ============================================================
# 5. CREATE TODO - POST API
# ============================================================

# @app.post() tells FastAPI to create a POST endpoint.
# "/todos" is the URL path of this endpoint.
# status_code=201 means the response indicates successful creation.
@app.post("/todos", status_code=201)

# Define the function that executes when someone sends a POST request.
# todo: TodoCreate receives and validates the request body.
# db: Session declares that db is a SQLAlchemy database session.
# Depends(get_db) tells FastAPI to provide that session.
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):

    # Create a new SQLAlchemy Todo object.
    # models.Todo refers to the Todo class inside models.py.
    new_todo = models.Todo(

        # Get the title value from the validated request data.
        title=todo.title,

        # Get the completed value from the validated request data.
        completed=todo.completed
    )

    # Add the new Todo object to the current database session.
    # This prepares the object to be inserted into MySQL.
    db.add(new_todo)

    # Commit the transaction.
    # This saves the new Todo record permanently in MySQL.
    db.commit()

    # Refresh the object using the latest values from MySQL.
    # This retrieves automatically generated values such as the ID.
    db.refresh(new_todo)

    # Return a response to the client after successful creation.
    return {

        # Return a success message.
        "message": "Todo added successfully",

        # Return the details of the newly created Todo.
        "data": {

            # Return the database-generated Todo ID.
            "id": new_todo.id,

            # Return the saved Todo title.
            "title": new_todo.title,

            # Return the saved completion status.
            "completed": new_todo.completed
        }
    }


# ============================================================
# 6. GET ALL TODOS - GET API
# ============================================================

# @app.get() tells FastAPI to create a GET endpoint.
# "/todos" is the URL path.
# This endpoint retrieves all Todo records from MySQL.
@app.get("/todos")

# Define the function that executes when someone sends a GET request.
# db receives a database session through Depends(get_db).
def get_todos(db: Session = Depends(get_db)):

    # Query the Todo table in MySQL.
    # models.Todo represents the todos table.
    # .all() retrieves all matching records.
    todos = db.query(models.Todo).all()

    # Create an empty Python list.
    # We will store the retrieved Todo records in this list.
    result = []

    # Loop through every Todo record retrieved from MySQL.
    # Each record is temporarily stored in the variable todo.
    for todo in todos:

        # append() adds an item to the result list.
        # We add each Todo record as a Python dictionary.
        result.append({

            # Get the ID of the current Todo record.
            "id": todo.id,

            # Get the title of the current Todo record.
            "title": todo.title,

            # Get the completion status of the current Todo record.
            "completed": todo.completed
        })

    # Return all retrieved Todo records to the client.
    return {

        # Return a success message.
        "message": "Todos retrieved successfully",

        # Return the list containing all Todo records.
        "data": result
    }


# ============================================================
# 7. UPDATE TODO BY ID - PUT API
# ============================================================

# @app.put() tells FastAPI to create a PUT endpoint.
# "/todos/{todo_id}" means the Todo ID comes from the URL.
# Example: PUT /todos/2
@app.put("/todos/{todo_id}")

# Define the function that updates an existing Todo.
def update_todo(

    # Receive the Todo ID from the URL.
    # int means the ID must be an integer.
    todo_id: int,

    # Receive the updated request body.
    # TodoCreate validates the title and completed fields.
    updated_todo: TodoCreate,

    # Receive a database session through the get_db dependency.
    db: Session = Depends(get_db)
):

    # Query the Todo table in MySQL.
    # filter() searches for a record matching the given condition.
    todo = db.query(models.Todo).filter(

        # Check whether the database record ID equals the URL ID.
        models.Todo.id == todo_id

    # first() returns the first matching record.
    # If no record matches, it returns None.
    ).first()

    # Check whether the requested Todo record exists.
    if todo is None:

        # Raise an HTTP error if the record does not exist.
        # status_code=404 means Not Found.
        raise HTTPException(

            # Return HTTP status code 404.
            status_code=404,

            # Return an error message to the client.
            detail="Todo not found"
        )

    # Update the title of the existing Todo record.
    # The new title comes from the request body.
    todo.title = updated_todo.title

    # Update the completed status of the existing Todo.
    # The new value comes from the request body.
    todo.completed = updated_todo.completed

    # Commit the updated changes to MySQL.
    db.commit()

    # Refresh the Todo object with the latest database values.
    db.refresh(todo)

    # Return the updated Todo record to the client.
    return {

        # Return a success message.
        "message": "Todo updated successfully",

        # Return the updated Todo details.
        "data": {

            # Return the Todo ID.
            "id": todo.id,

            # Return the updated title.
            "title": todo.title,

            # Return the updated completion status.
            "completed": todo.completed
        }
    }


# ============================================================
# 8. DELETE TODO BY ID - DELETE API
# ============================================================

# @app.delete() tells FastAPI to create a DELETE endpoint.
# "/todos/{todo_id}" means the ID comes from the URL.
# Example: DELETE /todos/2
@app.delete("/todos/{todo_id}")

# Define the function that deletes an existing Todo.
def delete_todo(

    # Receive the Todo ID from the URL.
    todo_id: int,

    # Receive a database session through the get_db dependency.
    db: Session = Depends(get_db)
):

    # Query the Todo table in MySQL.
    # Search for the record whose ID matches todo_id.
    todo = db.query(models.Todo).filter(

        # Compare the database record ID with the requested ID.
        models.Todo.id == todo_id

    # Return the first matching record.
    # Return None if no matching record exists.
    ).first()

    # Check whether the requested Todo exists.
    if todo is None:

        # Raise an HTTP error when the Todo does not exist.
        raise HTTPException(

            # HTTP 404 means the requested record was not found.
            status_code=404,

            # Send an error message to the client.
            detail="Todo not found"
        )

    # Mark the selected Todo object for deletion.
    # The deletion is not permanently committed yet.
    db.delete(todo)

    # Commit the transaction.
    # This permanently applies the deletion in MySQL.
    db.commit()

    # Return a success response after deletion.
    return {

        # Send a success message.
        "message": "Todo deleted successfully",

        # Return the ID of the deleted Todo.
        "id": todo_id
    }


# ============================================================
# 9. GET TODO BY ID - GET API
# ============================================================

# @app.get() creates a GET endpoint.
# "/todos/{todo_id}" receives the Todo ID from the URL.
# Example: GET /todos/2
@app.get("/todos/{todo_id}")

# Define the function to retrieve one Todo using its ID.
def get_todo_by_id(

    # Receive the Todo ID from the URL.
    todo_id: int,

    # Receive a database session through Depends(get_db).
    db: Session = Depends(get_db)
):

    # Query the Todo table in MySQL.
    todo = db.query(models.Todo).filter(

        # Find the record whose ID equals the requested ID.
        models.Todo.id == todo_id

    # Return the first matching record.
    # Return None if no matching record exists.
    ).first()

    # Check whether the requested Todo exists.
    if todo is None:

        # Raise HTTP 404 if the Todo was not found.
        raise HTTPException(

            # Set the HTTP status code to 404.
            status_code=404,

            # Return an error message.
            detail="Todo not found"
        )

    # Return the requested Todo record.
    return {

        # Return the Todo ID.
        "id": todo.id,

        # Return the Todo title.
        "title": todo.title,

        # Return the completion status.
        "completed": todo.completed
    }


# ============================================================
# 10. PYDANTIC MODEL FOR PARTIAL UPDATE
# ============================================================

# Create a separate Pydantic model named TodoUpdate.
# This model is used when partially updating a Todo with PATCH.
class TodoUpdate(BaseModel):

    # title can contain a string or None.
    # None is the default, so the user can leave this field out.
    title: str | None = None

    # completed can contain True, False, or None.
    # None is the default, so the user can leave this field out.
    completed: bool | None = None


# ============================================================
# 11. PARTIAL UPDATE TODO BY ID - PATCH API
# ============================================================

# @app.patch() tells FastAPI to create a PATCH endpoint.
# "/todos/{todo_id}" receives the Todo ID from the URL.
# PATCH is used to update only the fields supplied by the client.
# Example: PATCH /todos/2
@app.patch("/todos/{todo_id}")

# Define the function that partially updates an existing Todo.
def patch_todo(

    # Receive the Todo ID from the URL.
    todo_id: int,

    # Receive the fields that the client wants to update.
    # TodoUpdate validates the supplied fields.
    updated_data: TodoUpdate,

    # Receive a database session through the get_db dependency.
    db: Session = Depends(get_db)
):

    # Query the Todo table in MySQL.
    todo = db.query(models.Todo).filter(

        # Search for the Todo whose ID matches the URL ID.
        models.Todo.id == todo_id

    # Return the first matching record.
    # Return None if the record does not exist.
    ).first()

    # Check whether the requested Todo exists.
    if todo is None:

        # Raise an HTTP 404 error if no Todo was found.
        raise HTTPException(

            # Set the response status code to 404.
            status_code=404,

            # Return an error message.
            detail="Todo not found"
        )

    # Check whether the client supplied a new title.
    # If title is not None, update the existing title.
    if updated_data.title is not None:

        # Assign the new title to the existing Todo object.
        todo.title = updated_data.title

    # Check whether the client supplied a new completed value.
    # We use "is not None" so that False is also accepted.
    if updated_data.completed is not None:

        # Assign the new completed value to the existing Todo object.
        todo.completed = updated_data.completed

    # Commit all changes to MySQL.
    db.commit()

    # Refresh the Todo object with the latest database values.
    db.refresh(todo)

    # Return the updated Todo record to the client.
    return {

        # Return a success message.
        "message": "Todo partially updated successfully",

        # Return the updated Todo details.
        "data": {

            # Return the Todo ID.
            "id": todo.id,

            # Return the current Todo title.
            "title": todo.title,

            # Return the current completion status.
            "completed": todo.completed
        }
    }
