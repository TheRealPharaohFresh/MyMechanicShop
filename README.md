
# 🛠️ MyMechanicShop API

**MyMechanicShop** is a powerful RESTful backend API for managing an auto repair shop's workflow — from customer registration to mechanic assignment, service ticket tracking, and real-time inventory deduction. Built using Flask and SQLAlchemy with modern architecture and best practices.

---

## 📚 Table of Contents

- [🚀 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [✅ Features](#-features)
- [🔐 Authentication](#-authentication)
- [📦 API Endpoints](#-api-endpoints)
- [⚙️ Setup & Running](#️-setup--running)
- [🧪 Tests](#-tests)
- [📄 Swagger API Docs](#-swagger-api-docs)
- [🚧 Rate Limiting](#-rate-limiting)
- [🧠 Future Enhancements](#-future-enhancements)
- [👑 Author](#-author)

---

## 🚀 Tech Stack

- **Python 3.13**
- **Flask** – Backend framework
- **Flask SQLAlchemy** – ORM for database modeling
- **Marshmallow** – Validation and serialization
- **JWT (python-jose)** – Secure token-based authentication
- **Flask-Limiter** – Built-in rate limiting
- **Flask-Caching** – Caches inventory GET requests
- **SQLite** (Dev) – Easily swappable with PostgreSQL or MySQL
- **Pytest** – Unit testing
- **Swagger (OpenAPI)** – API documentation (`swagger.yaml`)

---

## 📁 Project Structure

```

MyMechanicShop/
│
├── app/
│   ├── blueprints/
│   │   ├── customer/           # Customer routes & schemas
│   │   ├── mechanic/           # Mechanic routes & schemas
│   │   ├── service\_ticket/     # Ticket routes, logic, rate limiting
│   │   └── inventory/          # Inventory CRUD + caching
│   ├── static/swagger.yaml     # OpenAPI documentation
│   ├── utils/                  # Shared utilities
│   ├── models.py               # SQLAlchemy models
│   └── __init__.py             # App factory
│
├── tests/                      # unittest test suite
├── config.py                   # App config (DB URI, secrets, etc.)
├── flask_app.py                # Optional database initialization entry point
├── requirements.txt            # Dependencies
└── README.md                   # You're here!

````

---

## ✅ Features

### 👥 Customers
- Register, view, update, delete
- View personal service tickets

### 🧑‍🔧 Mechanics
- Add/edit/remove mechanics
- Assign/remove to/from service tickets
- View all mechanics assigned to a ticket

### 📝 Service Tickets
- Create, update, delete tickets
- Attach/detach parts and mechanics
- Auto-deduct inventory when assigned
- Auto-refund when removed
- View tickets by ID or for current user

### 📦 Inventory
- Full CRUD operations
- GET requests are **cached**
- Inventory deducted automatically on assignment

---

## 🔐 Authentication

All sensitive endpoints use **JWT Bearer Token Authentication**:

```bash
Authorization: Bearer <your_token_here>
````

Token is returned upon successful customer registration/login.

---

## 📦 API Endpoints

| Resource            | Endpoint                            | Method(s)          | Description                                |
| ------------------- | ----------------------------------- | ------------------ | ------------------------------------------ |
| **Customers**       | `/customers`                        | GET / POST         | List or create customer                    |
|                     | `/customers/<id>`                   | GET / PUT / DELETE | CRUD for specific customer                 |
| **Mechanics**       | `/mechanics`                        | GET / POST         | List or add new mechanic                   |
|                     | `/mechanics/<id>`                   | GET / PUT / DELETE | CRUD for specific mechanic                 |
| **Service Tickets** | `/service_tickets`                          | GET / POST         | List or create service tickets             |
|                     | `/service_tickets/<id>`                     | GET / PUT / DELETE | Manage specific ticket                     |
|                     | `/service_tickets/my-tickets`               | GET                | Get current user's tickets                 |
|                     | `/service_tickets/<id>/mechanics`           | PUT / GET          | Bulk update or view mechanics for a ticket |
|                     | `/service_tickets/<id>/mechanics/<mech_id>` | DELETE             | Remove specific mechanic from ticket       |
|                     | `/service_tickets/<id>/inventory`            | PUT                | Add or remove inventory on ticket          |
| **Inventory**       | `/inventory`                        | GET / POST         | List (cached) / add inventory              |
|                     | `/inventory/<id>`                   | GET / PUT / DELETE | CRUD for specific inventory item           |

---

## ⚙️ Setup & Running

1. **Clone the repository:**

```bash
git clone https://github.com/TheRealPharaohFresh/MyMechanicShop.git
cd MyMechanicShop
```

2. **Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows, activate it with `venv\\Scripts\\activate` instead.

3. **Install dependencies:**

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. **Run the Flask development server:**

```bash
flask --app app run --debug
```

API will be running at: [http://localhost:5000](http://localhost:5000)
The Swagger UI is available at [http://localhost:5000/api/docs](http://localhost:5000/api/docs).

The Flask app uses an in-memory SQLite database by default when started through
the app factory. For a persistent database, set `SQLALCHEMY_DATABASE_URI` and
start the app with the matching configuration before running Flask.

---

## 🧪 Tests

With the virtual environment activated, run the unit tests using:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

Covers:

* Customer routes
* Mechanic routes
* Service ticket logic
* Inventory CRUD and deductions

---

## 📄 Swagger API Docs

Live interactive docs available using [Swagger Editor](https://editor.swagger.io/):

* Import `app/static/swagger.yaml` for full endpoint documentation
* Browse request/response structure and models

---

## 🚧 Rate Limiting (by IP)

| Endpoint                      | Limit     |
| ----------------------------- | --------- |
| PUT `/service_tickets/<id>/mechanics` | 3 per day |
| PUT `/service_tickets/<id>/inventory` | 3 per day |
| DELETE `/service_tickets/<id>`         | 5 per day |

---

## 🧠 Future Enhancements

* [x] JWT Token Auth
* [x] Inventory deduction/refund logic
* [x] Rate-limiting and caching
* [x] Unit testing
* [x] Swagger API documentation
* [ ] Admin vs Customer role support
* [ ] PDF/email receipts for service tickets
* [ ] Dashboard analytics (avg repair cost, usage trends)
* [ ] AI assistant for summarizing vehicle history

---

## 👑 Author

**PharaohFresh (Donald Clemons)**
🎓 Graduate @ Coding Temple
💻 Software Developer | 🎚️ Audio Engineer
📍 Atlanta, GA
📫 [donaldericclemons@gmail.com](mailto:donaldericclemons@gmail.com)






