
# 🏘 Rental Service – Apartment Rental Web App

A full-featured web application for posting, viewing, and managing apartment rental listings. Supports user authentication, filtering, editing, deletion, and adding new listings.

---

## ⚙️ Technologies

- Backend: **Python**, **Django**, **Django REST Framework**
- Auth: **JWT (SimpleJWT)** with cookie-based tokens
- Frontend: **React**, **Vite**, **Axios**
- Database: **PostgreSQL**
- Caching: **Redis**
- Containerization: **Docker**, **docker-compose**
- API Docs: **drf-spectacular** (`/api/v1/docs/`)

---

## 📁 Project Structure

```
.
├── backend/
│   ├── apps/
│   │   ├── users/
│   │   └── apartments/
│   ├── config/
│   └── manage.py
├── frontend/
│   ├── src/
│   └── vite.config.js
├── docker-compose.yml
├── README.md
```

---

## 🚀 Quick Start (Docker)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/rental-service.git
cd rental-service
```

### 2. Add environment files

- `backend/.env` — for Django settings
- `frontend/.env` (optional) — e.g., `VITE_API_URL`

### 3. Run the app

```bash
docker-compose up --build
```

Available at:

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend API: [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)
- API Docs: [http://localhost:8000/api/v1/docs/](http://localhost:8000/api/v1/docs/)

---

## 🔐 Authentication

- JWT authentication using `httpOnly` cookies
- Endpoints:
  - `POST /auth/login/` — Login
  - `POST /auth/logout/` — Logout
  - `POST /auth/refresh/` — Refresh token
  - `GET /auth/me/` — Get current user

---

## 🧩 Main API Endpoints

### Apartments `/api/v1/apartments/`

| Method | URL                        | Description                        | Auth Required |
|--------|----------------------------|------------------------------------|----------------|
| GET    | `/apartments/`            | List apartments                    | ❌              |
| POST   | `/apartments/`            | Create new apartment               | ✅              |
| GET    | `/apartments/{slug}/`     | Apartment details                  | ❌              |
| PUT    | `/apartments/{slug}/`     | Update (only owner)                | ✅              |
| DELETE | `/apartments/{slug}/`     | Delete (only owner)                | ✅              |

---

## 🧪 Testing

```bash
cd backend
pytest
```

---

## 📝 API Documentation

- Swagger UI: [http://localhost:8000/api/v1/docs/](http://localhost:8000/api/v1/docs/)
- Generate schema manually:

```bash
python manage.py spectacular --file schema.yaml
```

---

## 🐳 Useful Docker Commands

```bash
# Restart after changes
docker-compose down
docker-compose up --build

# Enter backend container
docker exec -it rental-service-backend-1 bash
```

---

## 📌 TODO / Improvements

- [ ] Client-side form validation
- [ ] Image upload for apartments
- [ ] Favorite listings feature
- [ ] CI/CD pipeline

---

## 📄 License

Provided as-is for educational purposes. MIT License.

---

## 📦 Usage Examples

### 🏠 Fetch Apartment Listings

```bash
curl http://localhost:8000/api/v1/apartments/
```

### 🔐 Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "yourpassword"}' \
     -c cookies.txt
```

### 🏗️ Create a New Apartment (Authenticated)

```bash
curl -X POST http://localhost:8000/api/v1/apartments/ \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Modern Studio",
           "description": "Close to city center.",
           "number_of_rooms": 1,
           "square": 35.5,
           "price": 1200
         }' \
     -b cookies.txt
```

### 🔄 Refresh Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh/ \
     -b cookies.txt
```

### 🚪 Logout

```bash
curl -X POST http://localhost:8000/api/v1/auth/logout/ \
     -b cookies.txt
```

---
