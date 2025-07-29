
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
│   ├── utils/                  # Auth, DB init, decorators, extensions
│   ├── models.py               # SQLAlchemy models
│   └── **init**.py             # App factory
│
├── tests/                      # Pytest unit tests (CRUD & logic)
├── swagger.yaml                # OpenAPI 2.0 documentation
├── config.py                   # App config (DB URI, secrets, etc.)
├── run.py                      # App entry point
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
| **Service Tickets** | `/tickets`                          | GET / POST         | List or create service tickets             |
|                     | `/tickets/<id>`                     | GET / PUT / DELETE | Manage specific ticket                     |
|                     | `/tickets/my-tickets`               | GET                | Get current user's tickets                 |
|                     | `/tickets/<id>/mechanics`           | PUT / GET          | Bulk update or view mechanics for a ticket |
|                     | `/tickets/<id>/mechanics/<mech_id>` | DELETE             | Remove specific mechanic from ticket       |
|                     | `/tickets/<id>/inventory`           | PUT                | Add or remove inventory on ticket          |
| **Inventory**       | `/inventory`                        | GET / POST         | List (cached) / add inventory              |
|                     | `/inventory/<id>`                   | GET / PUT / DELETE | CRUD for specific inventory item           |

---

## ⚙️ Setup & Running

1. **Clone the repo:**

```bash
git clone https://github.com/TheRealPharaohFresh/MyMechanicShop.git
cd MyMechanicShop
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the server:**

```bash
python run.py
```

API will be running at: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Tests

Run unit tests using:

```bash
pytest tests/
```

Covers:

* Customer routes
* Mechanic routes
* Service ticket logic
* Inventory CRUD and deductions

---

## 📄 Swagger API Docs

Live interactive docs available using [Swagger Editor](https://editor.swagger.io/):

* Import `swagger.yaml` for full endpoint documentation
* Browse request/response structure and models

---

## 🚧 Rate Limiting (by IP)

| Endpoint                      | Limit     |
| ----------------------------- | --------- |
| PUT `/tickets/<id>/mechanics` | 3 per day |
| PUT `/tickets/<id>/inventory` | 3 per day |
| DELETE `/tickets/<id>`        | 5 per day |

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






