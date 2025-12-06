# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. In production, you should implement one of:
- Token-based authentication (JWT)
- OAuth2
- API Key authentication

## Response Format

### Success Response

```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  ...
}
```

### Error Response

```json
{
  "error": "ValidationError",
  "message": "Invalid input",
  "details": {
    "email": ["This field is required."]
  }
}
```

### Paginated Response

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/v1/profiles/?page=2",
  "previous": null,
  "results": [...]
}
```

## Endpoints

### 1. List User Profiles

**GET** `/api/v1/profiles/`

List all user profiles with pagination, filtering, and search capabilities.

**Query Parameters:**
- `page` (integer): Page number for pagination (default: 1)
- `page_size` (integer): Number of results per page (default: 20)
- `search` (string): Search in email, first_name, last_name, phone_number
- `is_active` (boolean): Filter by active status
- `country` (string): Filter by country
- `state` (string): Filter by state
- `city` (string): Filter by city
- `ordering` (string): Order by field (prefix with `-` for descending)
  - Options: `created_at`, `updated_at`, `email`, `last_name`

**Example Requests:**

```bash
# Basic list
GET /api/v1/profiles/

# With search
GET /api/v1/profiles/?search=john

# With filters
GET /api/v1/profiles/?state=NY&is_active=true

# With ordering
GET /api/v1/profiles/?ordering=-created_at

# Combined
GET /api/v1/profiles/?search=john&state=NY&ordering=-created_at&page=2
```

**Response (200 OK):**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "john.doe@example.com",
      "full_name": "John Doe",
      "city": "New York",
      "state": "NY",
      "is_active": true,
      "created_at": "2025-12-06T12:00:00Z"
    }
  ]
}
```

---

### 2. Create User Profile

**POST** `/api/v1/profiles/`

Create a new user profile.

**Required Fields:**
- `email` (string, unique): Valid email address
- `first_name` (string, max 50): User's first name
- `last_name` (string, max 50): User's last name

**Optional Fields:**
- `phone_number` (string): Phone number in format +1234567890
- `address_line1` (string, max 255)
- `address_line2` (string, max 255)
- `city` (string, max 100)
- `state` (string, max 100)
- `postal_code` (string, max 20)
- `country` (string, max 100, default: "USA")
- `date_of_birth` (date, format: YYYY-MM-DD)
- `bio` (string, max 500)

**Request Body:**

```json
{
  "email": "jane.smith@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone_number": "+1234567890",
  "address_line1": "456 Oak Ave",
  "city": "Los Angeles",
  "state": "CA",
  "postal_code": "90001",
  "country": "USA",
  "date_of_birth": "1995-05-15",
  "bio": "Product designer with 5 years of experience"
}
```

**Response (201 Created):**

```json
{
  "id": 2,
  "email": "jane.smith@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "full_name": "Jane Smith",
  "phone_number": "+1234567890",
  "address_line1": "456 Oak Ave",
  "address_line2": null,
  "city": "Los Angeles",
  "state": "CA",
  "postal_code": "90001",
  "country": "USA",
  "full_address": "456 Oak Ave, Los Angeles, CA, 90001, USA",
  "date_of_birth": "1995-05-15",
  "bio": "Product designer with 5 years of experience",
  "is_active": true,
  "created_at": "2025-12-06T12:30:00Z",
  "updated_at": "2025-12-06T12:30:00Z"
}
```

**Error Response (400 Bad Request):**

```json
{
  "error": "ValidationError",
  "message": "Invalid input",
  "details": {
    "email": ["A profile with this email already exists."]
  }
}
```

---

### 3. Retrieve User Profile

**GET** `/api/v1/profiles/{id}/`

Retrieve a specific user profile by ID.

**Path Parameters:**
- `id` (integer): Profile ID

**Response (200 OK):**

```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "address_line1": "123 Main St",
  "address_line2": "Apt 4B",
  "city": "New York",
  "state": "NY",
  "postal_code": "10001",
  "country": "USA",
  "full_address": "123 Main St, Apt 4B, New York, NY, 10001, USA",
  "date_of_birth": "1990-01-01",
  "bio": "Software engineer",
  "is_active": true,
  "created_at": "2025-12-05T10:00:00Z",
  "updated_at": "2025-12-06T11:00:00Z"
}
```

**Error Response (404 Not Found):**

```json
{
  "detail": "Not found."
}
```

---

### 4. Update User Profile (Full Update)

**PUT** `/api/v1/profiles/{id}/`

Completely update a user profile. All fields (except read-only) must be provided.

**Path Parameters:**
- `id` (integer): Profile ID

**Request Body:**

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1987654321",
  "address_line1": "789 New Street",
  "city": "Boston",
  "state": "MA",
  "postal_code": "02101",
  "country": "USA",
  "date_of_birth": "1990-01-01",
  "bio": "Senior software engineer"
}
```

**Response (200 OK):** Full profile object with updated data

---

### 5. Update User Profile (Partial Update)

**PATCH** `/api/v1/profiles/{id}/`

Partially update a user profile. Only provided fields will be updated.

**Path Parameters:**
- `id` (integer): Profile ID

**Request Body:**

```json
{
  "city": "San Francisco",
  "state": "CA",
  "bio": "Senior software engineer at Tech Corp"
}
```

**Response (200 OK):** Full profile object with updated data

---

### 6. Delete User Profile

**DELETE** `/api/v1/profiles/{id}/`

Soft delete a user profile (marks as inactive, data is retained).

**Path Parameters:**
- `id` (integer): Profile ID

**Response (204 No Content):**

```json
{
  "message": "User profile deactivated successfully"
}
```

---

### 7. Get Active Profiles

**GET** `/api/v1/profiles/active/`

Retrieve only active user profiles.

**Query Parameters:** Same as List endpoint

**Response (200 OK):** Paginated list of active profiles

---

### 8. Search by Email

**GET** `/api/v1/profiles/search_by_email/?email={email}`

Search for a profile by email address.

**Query Parameters:**
- `email` (string, required): Email address to search

**Example:**

```bash
GET /api/v1/profiles/search_by_email/?email=john.doe@example.com
```

**Response (200 OK):** Single profile object

**Error Response (404 Not Found):**

```json
{
  "error": "Profile not found"
}
```

**Error Response (400 Bad Request):**

```json
{
  "error": "Email parameter is required"
}
```

---

### 9. Reactivate Profile

**POST** `/api/v1/profiles/{id}/reactivate/`

Reactivate a soft-deleted (inactive) profile.

**Path Parameters:**
- `id` (integer): Profile ID

**Response (200 OK):** Full profile object with `is_active=true`

**Error Response (400 Bad Request):**

```json
{
  "message": "Profile is already active"
}
```

---

## System Endpoints

### Health Check

**GET** `/health/`

Check the health status of the service.

**Response (200 OK):**

```json
{
  "status": "healthy",
  "database": "ok",
  "cache": "ok"
}
```

---

### API Documentation

**GET** `/api/docs/`

Interactive Swagger UI documentation.

---

### API Schema

**GET** `/api/schema/`

Download OpenAPI schema in JSON format.

---

## Rate Limiting

- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour

## Pagination

Default page size: 20 items
Maximum page size: 100 items

To customize page size:
```bash
GET /api/v1/profiles/?page_size=50
```

## Error Codes

- `200 OK`: Successful GET/PATCH/PUT
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Validation error or invalid input
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Field Validation

### Email
- Must be valid email format
- Must be unique
- Automatically converted to lowercase
- Whitespace trimmed

### Phone Number
- Format: `+1234567890` (9-15 digits)
- Optional `+` prefix
- Optional country code

### Date of Birth
- Format: `YYYY-MM-DD`
- Cannot be in the future

### Bio
- Maximum 500 characters

### Names (first_name, last_name)
- Maximum 50 characters each

## Examples with curl

```bash
# Create profile
curl -X POST http://localhost:8000/api/v1/profiles/ \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "city": "Seattle",
  "state": "WA"
}
EOF

# List profiles
curl http://localhost:8000/api/v1/profiles/

# Get specific profile
curl http://localhost:8000/api/v1/profiles/1/

# Update profile
curl -X PATCH http://localhost:8000/api/v1/profiles/1/ \
  -H "Content-Type: application/json" \
  -d '{"bio": "Updated bio"}'

# Delete profile
curl -X DELETE http://localhost:8000/api/v1/profiles/1/

# Search by email
curl "http://localhost:8000/api/v1/profiles/search_by_email/?email=test@example.com"

# Filter and search
curl "http://localhost:8000/api/v1/profiles/?state=CA&search=john&ordering=-created_at"
```
