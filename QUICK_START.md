# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Docker (Easiest)

```bash
# 1. Clone and setup
git clone <repo-url> && cd cc-mvp
cp .env.example .env

# 2. Start everything
docker-compose up -d

# 3. Access your API
open http://localhost:8000/api/docs/
```

That's it! Your API is running at http://localhost:8000

### Option 2: Local Development

```bash
# 1. Setup environment
cp .env.example .env
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure database
# Edit .env with your MySQL credentials

# 3. Run migrations
python manage.py migrate

# 4. Start server
python manage.py runserver
```

---

## 📋 Essential Commands

### Docker Commands
```bash
docker-compose up -d              # Start services
docker-compose down               # Stop services
docker-compose logs -f web        # View logs
docker-compose exec web bash      # Access container
```

### Django Commands
```bash
python manage.py migrate          # Run migrations
python manage.py createsuperuser  # Create admin user
python manage.py runserver        # Start dev server
python manage.py test            # Run tests
```

### Make Commands
```bash
make install      # Install dependencies
make migrate      # Run migrations
make run          # Start server
make test         # Run tests
make docker-up    # Start Docker containers
```

---

## 🔗 Important URLs

| Service | URL | Description |
|---------|-----|-------------|
| **API** | http://localhost:8000/api/v1/profiles/ | Main API endpoint |
| **Swagger** | http://localhost:8000/api/docs/ | Interactive API docs |
| **Admin** | http://localhost:8000/admin/ | Django admin panel |
| **Health** | http://localhost:8000/health/ | Health check |

---

## 📝 Quick API Examples

### Create a Profile
```bash
curl -X POST http://localhost:8000/api/v1/profiles/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "city": "New York",
    "state": "NY"
  }'
```

### Get All Profiles
```bash
curl http://localhost:8000/api/v1/profiles/
```

### Search by Email
```bash
curl "http://localhost:8000/api/v1/profiles/search_by_email/?email=john@example.com"
```

### Update Profile
```bash
curl -X PATCH http://localhost:8000/api/v1/profiles/1/ \
  -H "Content-Type: application/json" \
  -d '{"city": "Los Angeles"}'
```

### Delete Profile
```bash
curl -X DELETE http://localhost:8000/api/v1/profiles/1/
```

---

## 🛠️ Configuration

### Required Environment Variables
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=user_profile_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
```

Edit `.env` file for your configuration.

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **README.md** | Project overview and setup |
| **API_DOCUMENTATION.md** | Complete API reference |
| **DEPLOYMENT.md** | Production deployment |
| **PROJECT_SUMMARY.md** | Technical overview |
| **CODE_REVIEW_REPORT.md** | Code quality review |

---

## ✅ Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific tests
pytest apps/user_profile/tests.py -v
```

---

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check MySQL is running
mysql -u root -p

# Create database if needed
CREATE DATABASE user_profile_db;
```

### Port Already in Use
```bash
# Change port in docker-compose.yml or
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Docker Issues
```bash
# Rebuild containers
docker-compose down
docker-compose up -d --build

# Remove volumes
docker-compose down -v
```

---

## 🎯 Next Steps

1. **Create Superuser**: `docker-compose exec web python manage.py createsuperuser`
2. **Access Admin**: http://localhost:8000/admin/
3. **Try API**: http://localhost:8000/api/docs/
4. **Read Docs**: See README.md for detailed information

---

## 💡 Pro Tips

- Use Swagger UI for easy API testing
- Check health endpoint for service status
- Enable DEBUG=False in production
- Use proper SECRET_KEY in production
- Set up regular database backups

---

## 🆘 Need Help?

- Check logs: `docker-compose logs -f web`
- Read full docs: `README.md`
- View API docs: http://localhost:8000/api/docs/
- Check health: http://localhost:8000/health/

---

**Happy Coding! 🚀**
