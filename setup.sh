#!/bin/bash

echo "========================================="
echo "User Profile Microservice Setup"
echo "========================================="
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env file"
    else
        cp .env.example .env
        echo "✓ Created .env from .env.example"
    fi
else
    cp .env.example .env
    echo "✓ Created .env from .env.example"
fi

echo ""
echo "========================================="
echo "Configuration"
echo "========================================="
echo ""

# Generate secret key
echo "Generating Django SECRET_KEY..."
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Update .env file
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s|SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|" .env
else
    # Linux
    sed -i "s|SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|" .env
fi

echo "✓ Generated and set SECRET_KEY"

echo ""
echo "Please update the following in .env file:"
echo "  - DB_PASSWORD: Your MySQL password"
echo "  - DB_USER: Your MySQL username"
echo "  - ALLOWED_HOSTS: Your domain (if deploying to production)"
echo ""

read -p "Press Enter to continue..."

echo ""
echo "========================================="
echo "Choose Installation Method"
echo "========================================="
echo ""
echo "1) Docker (Recommended)"
echo "2) Local Development"
echo ""
read -p "Enter choice [1-2]: " choice

case $choice in
    1)
        echo ""
        echo "Starting Docker setup..."

        # Check if Docker is installed
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker is not installed. Please install Docker first."
            echo "Visit: https://docs.docker.com/get-docker/"
            exit 1
        fi

        if ! command -v docker-compose &> /dev/null; then
            echo "❌ Docker Compose is not installed. Please install Docker Compose first."
            echo "Visit: https://docs.docker.com/compose/install/"
            exit 1
        fi

        echo "✓ Docker and Docker Compose are installed"
        echo ""
        echo "Building and starting containers..."
        docker-compose up -d --build

        echo ""
        echo "Waiting for services to start..."
        sleep 10

        echo ""
        echo "Running migrations..."
        docker-compose exec web python manage.py migrate

        echo ""
        echo "✓ Setup complete!"
        echo ""
        echo "Access your application at:"
        echo "  - API: http://localhost:8000/api/v1/profiles/"
        echo "  - Swagger Docs: http://localhost:8000/api/docs/"
        echo "  - Admin: http://localhost:8000/admin/"
        echo "  - Health Check: http://localhost:8000/health/"
        echo ""
        echo "To create a superuser, run:"
        echo "  docker-compose exec web python manage.py createsuperuser"
        ;;

    2)
        echo ""
        echo "Setting up local development environment..."

        # Check Python version
        if ! command -v python3.12 &> /dev/null; then
            echo "❌ Python 3.12 is not installed."
            echo "Please install Python 3.12 first."
            exit 1
        fi

        echo "✓ Python 3.12 is installed"

        # Create virtual environment
        echo ""
        echo "Creating virtual environment..."
        python3.12 -m venv venv

        # Activate virtual environment and install dependencies
        echo "Installing dependencies..."
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt

        echo ""
        echo "⚠️  Before continuing, make sure:"
        echo "  1. MySQL is installed and running"
        echo "  2. Database 'user_profile_db' is created"
        echo "  3. .env file has correct database credentials"
        echo ""
        read -p "Press Enter when ready to run migrations..."

        # Run migrations
        echo ""
        echo "Running migrations..."
        python manage.py makemigrations
        python manage.py migrate

        echo ""
        echo "Creating logs directory..."
        mkdir -p logs

        echo ""
        echo "✓ Setup complete!"
        echo ""
        echo "To start the development server, run:"
        echo "  source venv/bin/activate"
        echo "  python manage.py runserver"
        echo ""
        echo "Then access your application at:"
        echo "  - API: http://localhost:8000/api/v1/profiles/"
        echo "  - Swagger Docs: http://localhost:8000/api/docs/"
        echo "  - Admin: http://localhost:8000/admin/"
        echo "  - Health Check: http://localhost:8000/health/"
        echo ""
        echo "To create a superuser, run:"
        echo "  python manage.py createsuperuser"
        ;;

    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "Setup Complete! 🎉"
echo "========================================="
echo ""
echo "For documentation, see:"
echo "  - README.md - Project overview and quick start"
echo "  - API_DOCUMENTATION.md - Complete API reference"
echo "  - DEPLOYMENT.md - Production deployment guide"
echo ""
