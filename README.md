# Retail Portal: Full Stack E-Commerce Platform

> HCLTech Python Full Stack Hackathon | One-day build | Sprint 0 deliverable (roadmap and approach)

**Team:** `<your name / team name>`
**Repo:** `<github repo link>`
**Live demo:** `<deployment link, added in Sprint 2>`

---

## 1. Problem Statement

Build a scalable e-commerce platform with:

- User management (sign-up, login)
- Product and category management (create, list, search, stock updates)
- A fast, intuitive shopping experience (home page grouped by category, in the style of a food-ordering app)
- Clear separation of UI, API, and database layers, with clear documentation

**Primary objective:** a working Single Page Application (SPA) where **admins** manage the catalog and stock, and **customers** browse, search, order, and re-order, backed by a secure, well-documented API.

---

## 2. Solution Approach

| Layer | Choice | Why |
|---|---|---|
| Frontend | React + Vite (SPA), React Router, Tailwind CSS | Fast dev server, built-in lazy loading (`React.lazy`), clean styling |
| Backend | Python 3.12 + FastAPI | Auto-generated Swagger docs, async, simple JWT/RBAC |
| Database | PostgreSQL (Neon cloud or local) | Relational data: orders, stock history, categories |
| ORM / Migrations | SQLAlchemy + Alembic | Schema versioning |
| Auth | JWT + Role-Based Access Control + API key | Meets all three auth requirements |
| Testing | Postman collection + pytest | Required validation artifact |
| CI/CD | GitHub Actions | Required pipeline configuration |
| Deployment (nice to have) | Render (API), Vercel (UI), Neon (DB) | Free tiers |

### Architecture

```
React SPA (Vercel)  --HTTPS/JSON-->  FastAPI (Render)  --SQLAlchemy-->  PostgreSQL (Neon)
   lazy loading                      JWT + RBAC + API key               products, stock_history,
   pagination / load more            validation + error codes           orders, users
```

---

## 3. Features and Priority

**P1 = must ship (MVP) | P2 = if time allows | P3 = stretch**

### User Management
- [ ] P1: Sign-up and login pages (JWT)
- [ ] P1: Roles: `admin` and `customer`

### Admin: Product and Category Management
- [ ] P1: Category CRUD (ID, name, logo, description)
- [ ] P1: Product CRUD (ID, image upload, title, description, cost, tax %)
- [ ] P1: Stock update screen (quick +/- and set quantity)
- [ ] P1: Stock history log (who changed what, when)
- [ ] P1: Paginated admin product list

### Customer: Shopping Experience
- [ ] P1: Home page with products grouped by category
- [ ] P1: Category-based product listing
- [ ] P1: Fuzzy search by product name or category
- [ ] P1: Breadcrumb navigation
- [ ] P1: Lazy loading with a "Load more" button
- [ ] P1: Cart and place order
- [ ] P1: Order history
- [ ] P2: Quick re-order from past orders
- [ ] P3: Product combos and "add-on" options

### Backend, Quality and DevOps
- [ ] P1: Role-based access control on all write endpoints
- [ ] P1: API key authentication (`X-API-Key` header)
- [ ] P1: Consistent HTTP status codes and error codes
- [ ] P1: Postman collection exported into `/postman`
- [ ] P1: GitHub Actions CI pipeline (lint and test)
- [ ] P1: README and API documentation
- [ ] P2: Cloud deployment
- [ ] P2: Docker setup

---

## 4. Folder Structure

```
retail-portal/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/          # config, security (JWT, hashing), dependencies
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   ├── routers/       # auth, categories, products, stock, orders
│   │   ├── services/      # business logic (search, stock, orders)
│   │   └── errors.py      # custom exceptions and error codes
│   ├── tests/
│   ├── alembic/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── src/
│       ├── pages/         # Home, Category, Search, Cart, Orders, Admin/*
│       ├── components/    # ProductCard, Breadcrumb, Pagination, LoadMore
│       ├── api/           # axios client
│       └── routes.jsx     # lazy-loaded routes
├── postman/               # exported Postman collection and environment
├── .github/workflows/ci.yml
└── README.md
```

---

## 5. Database Schema

| Table | Key columns |
|---|---|
| `users` | id, name, email (unique), password_hash, role, created_at |
| `categories` | id, name (unique), logo_url, description |
| `products` | id, category_id (FK), title, description, image_url, cost, tax_percent, stock_quantity, is_active, created_at |
| `stock_history` | id, product_id (FK), old_qty, new_qty, change, reason, changed_by (FK users), created_at |
| `orders` | id, user_id (FK), subtotal, tax_total, total, status, created_at |
| `order_items` | id, order_id (FK), product_id (FK), quantity, unit_price, tax_percent |
| `combos` and `combo_items` *(P3)* | combo definitions and the products inside them |
| `product_addons` *(P3)* | product_id, addon_product_id |

---

## 6. API Specification

Base path: `/api/v1`. Interactive docs are at `/docs` (Swagger).

### Auth
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/auth/signup` | Public | Register a customer |
| POST | `/auth/login` | Public | Returns a JWT access token |
| GET | `/auth/me` | Authenticated | Current user profile |

### Categories
| Method | Endpoint | Access |
|---|---|---|
| GET | `/categories` | Public |
| GET | `/categories/{id}` | Public |
| POST | `/categories` | Admin |
| PUT | `/categories/{id}` | Admin |
| DELETE | `/categories/{id}` | Admin |

### Products
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/products?category_id=&page=&limit=` | Public | Paginated listing |
| GET | `/products/search?q=&category_id=` | Public | Fuzzy search |
| GET | `/products/{id}` | Public | Product detail |
| POST | `/products` | Admin | Create (multipart for image) |
| PUT | `/products/{id}` | Admin | Update |
| DELETE | `/products/{id}` | Admin | Soft delete |

### Stock
| Method | Endpoint | Access |
|---|---|---|
| PATCH | `/products/{id}/stock` | Admin |
| GET | `/products/{id}/stock-history` | Admin |

### Orders
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/orders` | Customer | Place an order (reduces stock) |
| GET | `/orders` | Customer | Own order history (paginated) |
| GET | `/orders/{id}` | Customer / Admin | Order detail |
| POST | `/orders/{id}/reorder` | Customer | Rebuild a cart from a past order |

### Authentication and Authorization
- **JWT:** `Authorization: Bearer <token>`, signed with a secret from `.env`, with an expiry.
- **RBAC:** a FastAPI dependency checks `role` on each route (`admin` or `customer`).
- **API key:** `X-API-Key` header, validated against an environment variable.
- **Passwords:** hashed with bcrypt, never stored in plain text.

### Error Handling

All errors share one JSON shape:

```json
{ "error": { "code": "PRODUCT_NOT_FOUND", "message": "Product 42 does not exist", "status": 404 } }
```

| HTTP | Error code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Bad input |
| 401 | `INVALID_CREDENTIALS` / `TOKEN_EXPIRED` | Login failed or token invalid |
| 401 | `API_KEY_MISSING` / `API_KEY_INVALID` | API key check failed |
| 403 | `FORBIDDEN` | Role not allowed |
| 404 | `PRODUCT_NOT_FOUND` / `CATEGORY_NOT_FOUND` / `ORDER_NOT_FOUND` | Resource missing |
| 409 | `EMAIL_ALREADY_EXISTS` / `INSUFFICIENT_STOCK` | Conflict |
| 500 | `INTERNAL_ERROR` | Unexpected failure |

---

## 7. Sprint Roadmap

### Sprint 0: Planning and Setup (first 1 to 1.5 hrs)
- [x] Understand the problem statement
- [x] Finalize approach and tech stack (this README)
- [ ] Create the GitHub repo, push this README
- [ ] Backend: virtual environment, install libraries, FastAPI "hello" endpoint
- [ ] Frontend: Vite + React scaffold, Tailwind, React Router
- [ ] Database: create the Neon (or local) DB, confirm connection, create tables
- [ ] Task list finalized (the checklist in section 3)

### Sprint 1: Core Development (next 3 to 4 hrs)
1. Auth: signup, login, JWT, roles
2. Categories and products CRUD (admin)
3. Stock update and stock history
4. Product listing with pagination and search
5. Frontend: login, admin screens, home page by category, breadcrumbs, load more
6. Cart, place order, order history
7. Midpoint check-in with chapter members

**Deliverable:** working prototype with core features integrated.

### Sprint 2: Refinement, Testing, Submission and Demo (final 1 hr)
- [ ] Debug and polish the UX
- [ ] Export the Postman collection to `/postman`
- [ ] GitHub Actions CI working
- [ ] Deploy (Render, Vercel, Neon), if time allows
- [ ] Finalize the README with screenshots and the demo link
- [ ] Prepare the short pitch

**Deliverable:** a fully functional MVP with clear documentation.

---

## 8. Local Setup

### Prerequisites
Python 3.12+, Node.js (LTS), Git, PostgreSQL (or a Neon account), Postman.

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
cp .env.example .env           # fill in DATABASE_URL, JWT_SECRET, API_KEY
alembic upgrade head
uvicorn app.main:app --reload
```
API runs at `http://localhost:8000`, Swagger at `http://localhost:8000/docs`.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
App runs at `http://localhost:5173`.

### Environment variables (`backend/.env`)
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
JWT_SECRET=change-me
JWT_EXPIRE_MINUTES=60
API_KEY=change-me
```

---

## 9. Testing and Validation

- **Postman:** import `postman/retail-portal.postman_collection.json`. It covers auth, CRUD, search, stock, orders, and error cases.
- **Automated:** `cd backend && pytest`
- **CI:** every push runs lint and tests via `.github/workflows/ci.yml`.

---

## 10. Judging Criteria Mapping

| Criteria | How we address it |
|---|---|
| Technical Execution | Layered architecture, RBAC, JWT, validation, consistent errors, CI/CD |
| Innovation and Impact | Fuzzy search, quick re-order, stock history, combos and add-ons |
| User Experience | SPA, lazy loading, load more, breadcrumbs, category-first home page |
| Functionality | End-to-end flow: browse, search, order, track, admin stock management |

---

## 11. Branching and Git Workflow

- `main`: stable, demo-ready
- `dev`: integration branch
- `feature/<name>`: one branch per feature, merged into `dev` by pull request

---

## 12. Pitch (one-liner)

A fast, secure, category-first retail portal where admins keep the catalog and stock accurate in seconds, and customers find products quickly, order easily, and re-order in one click.
