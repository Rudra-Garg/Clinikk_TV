# Clinikk TV Backend Service (POC)

Clinikk TV Backend Service is a proof-of-concept implementation providing media (video and audio) content management and streaming capabilities with user authentication. The service is built using Python and FastAPI and integrates with PostgreSQL and AWS S3.

## Table of Contents
- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [High-Level Design (HLD)](#high-level-design-hld)
- [Low-Level Design (LLD)](#low-level-design-lld)
- [API Documentation](#api-documentation)
- [Installation and Running](#installation-and-running)
- [Testing](#testing)
- [Personal Motivation and Technology Choice](#personal-motivation-and-technology-choice)
- [Future Optimizations](#future-optimizations)


## Overview
This backend service supports:
- **Media Content Management:** Create, update, delete, retrieve, and stream audio/video content.
- **User Authentication:** Registration and JWT-based login.
- **Storage Integration:** Media uploads to AWS S3.

## Technology Stack
- **Language/Framework:** Python with FastAPI
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **Storage:** AWS S3
- **Authentication:** JWT Tokens
- **Containerization:** Docker and Docker Compose

## High-Level Design (HLD)
The system is designed with modularity and scalability in mind:
- **API Layer:** FastAPI endpoints exposed via routers.
- **Controller Layer:** Business logic handling // coordination between endpoints and services.
- **Service Layer:** Implementation of features such as authentication, content management, and storage integration.
- **Data Access Layer:** SQLAlchemy models for interacting with PostgreSQL.
- **Storage Integration:** AWS S3 is used for file uploads and serving media content.

## Low-Level Design (LLD)
- **Routers:**  
  - Located in `routes/content_routes.py` and `routes/auth_routes.py`, they map HTTP endpoints to their corresponding controllers.
- **Controllers:**  
  - For example, `ContentController.create_content` handles file upload, communication with the storage service, and database record creation.
- **Services:**  
  - `StorageService` (in `services/storage_service.py`) encapsulates file storage operations with AWS S3.
  - `AuthService` (in `services/auth_service.py`) handles user registration, login, and password management.
- **Data Models:**  
  - SQLAlchemy models in `models/content.py` and `models/user.py` define the structure of content and user data.

## API Documentation
FastAPI's automatic API docs come built-in. Once the service is running, visit:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Example Endpoints
- **Health Check:** `GET /health`
- **Create Content:** `POST /content/`
  - Accepts form-data (title, description, content_type, duration, thumbnail_url) and a media file.
- **Register User:** `POST /auth/register`
- **User Login:** `POST /auth/token`

## Installation and Running
### Using Docker Compose
Ensure you have a valid `.env` file in your repository with the required settings, then run:

```bash
docker-compose up --build
```

### Running Locally
1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Testing
Run the tests using pytest:
```bash
pytest
```

## Personal Motivation and Technology Choice
While Node.js was mentioned as a preferred option, I opted for Python with FastAPI based on the following reasons:
- **Extensive Experience with Python:** I have a strong background in Python development, and this expertise enabled me to quickly leverage its rich ecosystem and robust libraries to build an efficient and scalable backend service.
- **Benefits of FastAPI:** FastAPI provides automatic API documentation, excellent asynchronous support, and rapid development capabilities, making it ideal for creating modern and high-performance backend services.
- **Scalability and Maintainability:** Python with FastAPI facilitates a modular and clean architecture, which is critical for building scalable applications.

