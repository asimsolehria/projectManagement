# Django Project Management System API

This is a Django-based Project Management System that allows users to create projects, assign multiple users to projects, and perform CRUD operations on tasks. The system uses JWT (JSON Web Token) for authentication and implements soft delete functionality for both projects and tasks.

## Features

- User authentication and authorization using JWT.
- Project management: Create projects, assign users to projects.
- Task management: CRUD operations on tasks within projects.
- Soft delete: Mark projects and tasks as deleted without permanently removing them.
- REST API endpoints for all operations.

## Requirements

- asgiref==3.8.1
- dj-database-url==2.0.0
- Django==4.2.16
- django-cockroachdb==4.2
- djangorestframework==3.15.2
- djangorestframework-simplejwt==5.3.1
- psycopg2-binary==2.9.7
- PyJWT==2.9.0
- python-dotenv==1.0.1
- sqlparse==0.5.1
- typing_extensions==4.12.2


## Setup Instructions

### Step 1: Clone the repository

```bash
git clone git@github.com:asimsolehria/projectManagement.git
cd projectManagement
git checkout develop 
git pull origin develop 


