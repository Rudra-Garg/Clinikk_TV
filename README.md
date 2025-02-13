# Clinikk TV Backend Service (POC)

Clinikk TV Backend Service is a proof-of-concept implementation that provides robust media (video and audio) content management and streaming capabilities along with user authentication. The service is built using Python and FastAPI, and it integrates with PostgreSQL for data storage and AWS S3 for media storage.

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
  - [High-Level Design (HLD)](#high-level-design-hld)
  - [Low-Level Design (LLD)](#low-level-design-lld)
- [API Documentation](#api-documentation)
- [Installation and Running](#installation-and-running)
  - [Using Docker Compose](#using-docker-compose)
  - [Running Locally](#running-locally)
- [Testing](#testing)
- [Personal Motivation and Technology Choice](#personal-motivation-and-technology-choice)

## Overview
Clinikk TV Backend Service supports:
- **Media Content Management:** Create, update, delete, retrieve, and stream video/audio content.
- **User Authentication:** Secure user registration and JWT-based login.
- **Storage Integration:** Media file uploads and streaming via AWS S3.

## Key Features
- **Fast Development:** Leverages FastAPI's automatic API documentation and asynchronous support.
- **Scalable Architecture:** A modular design dividing responsibilities into API, Controller, Service, and Data Access layers.
- **Secure:** Uses industry-standard JWT tokens and bcrypt-based password hashing for robust security.
- **Containerized Deployment:** Ready to run via Docker and Docker Compose for easy deployment.

## Technology Stack
- **Language & Framework:** Python, FastAPI
- **Database:** PostgreSQL (using SQLAlchemy ORM)
- **Storage:** AWS S3
- **Authentication:** JWT Tokens
- **Containerization:** Docker and Docker Compose

## Architecture

### High-Level Design (HLD)
The system follows a layered architecture:
- **API Layer:** Exposes endpoints with FastAPI routers.
- **Controller Layer:** Contains business logic for coordinating requests and services.
- **Service Layer:** Implements core features such as media processing, authentication, and S3 interactions.
- **Data Access Layer:** Uses SQLAlchemy models for database CRUD operations.
- **Storage Integration:** Manages AWS S3 file operations including uploads and presigned URL generation.

### Low-Level Design (LLD)
- **Routers:**  
  - Located in `routes/content_routes.py` and `routes/auth_routes.py`, they map HTTP requests to controller functions.
- **Controllers:**  
  - For instance, `ContentController.create_content` handles file validation, S3 uploads, and saving the record to PostgreSQL.
- **Services:**  
  - `StorageService` (in `services/storage_service.py`) abstracts AWS S3 operations.
  - `AuthService` (in `services/auth_service.py`) manages user registration, authentication, and secure password handling.
- **Data Models:**  
  - Defined in `models/content.py` and `models/user.py`, they establish the schema for content and user data.

## API Documentation
Once the service is running, FastAPI automatically generates interactive API documentation:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Example Endpoints
- **Health Check:** `GET /health`
- **Create Content:** `POST /content/`  
  Accepts form-data parameters (title, description, content_type, duration, thumbnail_url) along with a media file upload.
- **User Registration:** `POST /auth/register`
- **User Login:** `POST /auth/token`

## Installation and Running

### Using Docker Compose
Ensure you have a valid `.env` file configured with your PostgreSQL and AWS S3 settings. Then, run:
```bash
docker-compose up --build
```

### Running Locally
1. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Testing
Run all tests using pytest:
```bash
pytest
```

## Personal Motivation and Technology Choice
While Node.js was an option, I chose Python with FastAPI due to:
- **Extensive Python Experience:** My background enables rapid development using Python's rich ecosystem.
- **FastAPI Benefits:** Automatic API docs, asynchronous support, and concise code structure make it ideal for modern backend services.
- **Clean Architecture:** A modular design supports scalability and maintainability in complex applications.
