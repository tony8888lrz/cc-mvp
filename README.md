# User Profile Microservice

A professional Django-based RESTful API microservice for managing user profiles, built with Python 3.12 and MySQL.

## Features

- **RESTful API Design**: Full CRUD operations for user profile management
- **Microservice Architecture**: Containerized with Docker, health checks, and proper logging
- **Database**: MySQL backend with proper indexing and query optimization
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Validation**: Comprehensive input validation and error handling
- **Security**: Production-ready security configurations
- **Testing**: Comprehensive test suite with pytest
- **Soft Delete**: Data retention with soft delete functionality

## Technology Stack

- **Python**: 3.12
- **Framework**: Django 5.0.9
- **API Framework**: Django REST Framework 3.15.2
- **Database**: MySQL 8.0
- **Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest, pytest-django

## API Endpoints

### User Profile Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/profiles/` | List all user profiles (paginated) |
| POST | `/api/v1/profiles/` | Create a new user profile |
| GET | `/api/v1/profiles/{id}/` | Retrieve a specific profile |
| PUT | `/api/v1/profiles/{id}/` | Update a profile (full update) |
| PATCH | `/api/v1/profiles/{id}/` | Partially update a profile |
| DELETE | `/api/v1/profiles/{id}/` | Soft delete a profile |
| GET | `/api/v1/profiles/active/` | Get active profiles only |
| GET | `/api/v1/profiles/search_by_email/?email=<email>` | Search profile by email |
| POST | `/api/v1/profiles/{id}/reactivate/` | Reactivate a deactivated profile |

### System Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health/` | Health check endpoint |
| GET | `/api/docs/` | Swagger UI documentation |
| GET | `/api/schema/` | OpenAPI schema |
| GET | `/admin/` | Django admin interface |

## Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cc-mvp
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - API: http://localhost:8000/api/v1/profiles/
   - Swagger Docs: http://localhost:8000/api/docs/
   - Admin: http://localhost:8000/admin/
   - Health Check: http://localhost:8000/health/

### Option 2: Local Development

1. **Prerequisites**
   - Python 3.12
   - MySQL 8.0
   - pip

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your MySQL configuration
   ```

4. **Create MySQL database**
   ```sql
   CREATE DATABASE user_profile_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=user_profile_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Service Configuration
SERVICE_NAME=user-profile-service
SERVICE_VERSION=1.0.0
```

## API Usage Examples

### Create a User Profile

```bash
curl -X POST http://localhost:8000/api/v1/profiles/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "address_line1": "123 Main St",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "country": "USA",
    "date_of_birth": "1990-01-01",
    "bio": "Software engineer"
  }'
```

### List All Profiles

```bash
curl http://localhost:8000/api/v1/profiles/
```

### Get a Specific Profile

```bash
curl http://localhost:8000/api/v1/profiles/1/
```

### Update a Profile

```bash
curl -X PATCH http://localhost:8000/api/v1/profiles/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "city": "San Francisco",
    "state": "CA"
  }'
```

### Search by Email

```bash
curl "http://localhost:8000/api/v1/profiles/search_by_email/?email=john.doe@example.com"
```

### Filter Profiles

```bash
# Filter by state
curl "http://localhost:8000/api/v1/profiles/?state=NY"

# Search by name
curl "http://localhost:8000/api/v1/profiles/?search=John"

# Get active profiles only
curl http://localhost:8000/api/v1/profiles/active/
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific test file
pytest apps/user_profile/tests.py

# Run with verbose output
pytest -v
```

## Makefile Commands

The project includes a Makefile for common operations:

```bash
make install       # Install dependencies
make migrate       # Run database migrations
make run           # Run development server
make test          # Run tests
make clean         # Clean Python cache files
make docker-build  # Build Docker images
make docker-up     # Start Docker containers
make docker-down   # Stop Docker containers
make setup-env     # Copy .env.example to .env
```

## Project Structure

```
cc-mvp/
├── config/                 # Project configuration
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL routing
│   ├── wsgi.py            # WSGI config
│   └── asgi.py            # ASGI config
├── apps/                   # Application modules
│   └── user_profile/      # User profile app
│       ├── models.py      # Database models
│       ├── serializers.py # API serializers
│       ├── views.py       # API views
│       ├── urls.py        # App URL routing
│       ├── admin.py       # Admin configuration
│       ├── exceptions.py  # Custom exception handlers
│       └── tests.py       # Test suite
├── logs/                   # Application logs
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose config
├── pytest.ini             # Pytest configuration
├── Makefile               # Common commands
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Microservice Best Practices

This service implements several microservice best practices:

1. **Health Checks**: `/health/` endpoint for monitoring
2. **Logging**: Structured logging with configurable levels
3. **Environment Configuration**: 12-factor app principles
4. **Containerization**: Docker support for easy deployment
5. **API Versioning**: Versioned API endpoints (`/api/v1/`)
6. **Documentation**: Auto-generated OpenAPI documentation
7. **Error Handling**: Consistent error response format
8. **Data Retention**: Soft delete for data recovery
9. **Security**: Production-ready security configurations
10. **Testing**: Comprehensive test coverage

## Security Features

- CSRF protection
- XSS protection
- SQL injection prevention (ORM)
- Input validation and sanitization
- CORS configuration for microservice communication
- Secure production settings (HTTPS, secure cookies)
- Rate limiting (configurable)
- Email normalization (lowercase, trimmed)

## Performance Optimizations

- Database indexing on frequently queried fields
- Query optimization with `select_related` and `prefetch_related`
- Pagination for large result sets
- Atomic transactions for data consistency
- Efficient serializers for different use cases

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Use a strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` properly
4. Use environment-specific database credentials
5. Set up SSL/TLS certificates
6. Configure proper logging and monitoring
7. Set up backup strategies for MySQL
8. Use Gunicorn or uWSGI as WSGI server
9. Set up reverse proxy (Nginx/Apache)
10. Enable security settings in `settings.py`

## License

MIT License

## Support

For issues, questions, or contributions, please open an issue in the repository.
