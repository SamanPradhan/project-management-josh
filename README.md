# Task Management API

## Overview
A Django REST Framework-based Task Management API supporting user and task management with custom user model and multi-user task assignment.

## Features
- Custom user management
- Task creation, updating, and tracking
- Multi-user task assignment
- RESTful API endpoints for users and tasks

## Prerequisites
- Python 3.8+
- pip
- Django
- Django REST Framework

## Project Setup

### 1. Install Dependencies

pip install -r requirements.txt


### 2. Database Setup

python manage.py makemigrations
python manage.py migrate


### 3. Create Superuser

python manage.py createsuperuser


### 4. Run Server

python manage.py runserver


## API Endpoints

### User Endpoints
- `GET /api/users/` - List users
- `POST /api/users/` - Create user
- `GET /api/users/{id}/` - Retrieve user
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Task Endpoints
- `GET /api/tasks/` - List tasks
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}/` - Retrieve task
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task

### Custom Endpoints
- `GET /api/tasks/assigned-to/{user_id}/` - Get tasks for specific user

## Sample API Requests

### Create User

POST /api/users/
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "mobile": "1234567890",
  "password": "securepassword"
}


### Create Task

POST /api/tasks/
{
  "name": "Fix Login Bug",
  "description": "Users are unable to login",
  "task_type": "bug",
  "status": "pending"
}


## Test Credentials
- **Admin Email**: admin@example.com
- **Admin Password**: adminpass


## Environment
- Development Server: http://127.0.0.1:8000/
- Admin Interface: http://127.0.0.1:8000/admin/