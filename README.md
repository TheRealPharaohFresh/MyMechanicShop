# 🛠️ MyMechanicShop Backend

MyMechanicShop is a RESTful backend API for managing auto repair shops — enabling customers, mechanics, service tickets, and inventory tracking. Built with Flask and SQLAlchemy, it features robust token-based auth, modular architecture, caching, rate limiting, and real-time inventory deduction.

---

## 📁 Project Structure

MyMechanicShop/
│
├── app/
│ ├── blueprints/
│ │ ├── customer/ # Customer routes & schemas
│ │ ├── mechanic/ # Mechanic routes & schemas
│ │ ├── service_ticket/ # Ticket routes, inventory logic, rate limiting
│ │ └── inventory/ # Inventory CRUD with caching
│ ├── utils/ # Token auth, DB init, extensions
│ ├── models.py # SQLAlchemy models + relationships
│ └── init.py # App factory pattern
│
├── tests/ # Unit tests for all major endpoints
├── swagger.yaml # Swagger/OpenAPI 2.0 spec for the entire API
├── config.py # Configs (DB URI, secret keys, etc.)
├── run.py # App entry point
├── requirements.txt # Python dependencies
├── .gitignore
└── README.md # You're here!

markdown
Copy
Edit

---

## 🔧 Tech Stack

- **Python 3**
- **Flask (Backend API)**
- **Flask SQLAlchemy (ORM)**
- **Marshmallow (Validation/Serialization)**
- **JWT (Token authentication)**
- **Flask-Limiter (Rate limiting)**
- **Flask-Caching (Cached inventory endpoints)**
- **SQLite (Dev DB — PostgreSQL/MySQL ready)**
- **Blueprints for modular routing**
- **Swagger/OpenAPI 2.0**

---

## ✅ Features

### 🔐 Authentication
- JWT-based token auth (`Bearer <token>`)
- Token-protected routes for customer-specific access

### 👤 Customers
- Register, view, update, and delete customers
- Retrieve own service tickets via token

### 🧑‍🔧 Mechanics
- Add/edit/delete mechanics
- Assign mechanics to service tickets
- Remove mechanics from specific tickets
- List all mechanics assigned to a ticket

### 📝 Service Tickets
- Create new service tickets with mechanic + part associations
- Add/remove inventory parts from a ticket
- Auto-deduct and refund inventory quantities
- Get tickets by ID or fetch all
- Fetch tickets only for logged-in customer
- Rate limiting on sensitive endpoints

### 📦 Inventory
- Full CRUD: add, get, update, delete
- Cached GET requests (`/inventory`) for performance
- Quantity auto-adjusted when attached to tickets

---

## 📄 API Documentation

### Swagger/OpenAPI
- The full API is documented in [`swagger.yaml`](./swagger.yaml)
- Use Swagger UI or Postman to import and explore all endpoints

---

## 🧪 Testing

### Run Unit Tests

```bash
pytest tests/
Test Coverage
Full CRUD tested for:

/customers

/mechanics

/inventory

/tickets and associated routes (/mechanics, /inventory)

Includes:

Auth-protected routes

Edge cases (bad inputs, missing fields)

Token validation

Rate limit behaviors

🚀 Running the App
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the Server

bash
Copy
Edit
python run.py
App will launch at: http://localhost:5000

🔁 API Overview
Resource	Endpoint	Method	Description
Customers	/customers	GET/POST	List all / Register new customer
/customers/<id>	GET/PUT/DELETE	Get, update, or delete a customer
Mechanics	/mechanics	GET/POST	List all / Add new mechanic
/mechanics/<id>	GET/PUT/DELETE	Get, update, or delete a mechanic
Service Tickets	/tickets	GET/POST	List or create service tickets
/tickets/<id>	GET/PUT/DELETE	Get, update, or delete ticket
/tickets/my-tickets	GET	Get logged-in customer's tickets
/tickets/<id>/mechanics	PUT/GET	Bulk update / get mechanics on a ticket
/tickets/<id>/mechanics/<id>	DELETE	Remove a specific mechanic
/tickets/<id>/inventory	PUT	Add/remove inventory parts on a ticket
Inventory	/inventory	GET/POST	List (cached) / Add inventory
/inventory/<id>	GET/PUT/DELETE	Retrieve / Update / Delete inventory

🚧 Rate Limiting (Example Limits)
Endpoint	Limit
PUT /tickets/<id>/mechanics	3 per day
PUT /tickets/<id>/inventory	3 per day
DELETE /tickets/<id>	5 per day

🧠 Future Enhancements
✅ JWT Auth (done)

✅ Add unit + integration tests

✅ Swagger/OpenAPI spec (done)

🔐 Admin/User role differentiation

📊 Dashboard metrics (avg repair cost, revenue)

🧠 AI Assistant using RAG to summarize service history

🧾 Email receipts or PDF service logs

👑 Author
PharaohFresh (Donald Clemons)
🎓 Coding Temple Graduate
💻 Software Developer | 🎚️ Audio Engineer
📍 Atlanta, GA
📫 donaldericclemons@gmail.com

vbnet
Copy
Edit

Let me know if you want the README turned into a Markdown file or auto-linked with badges like `pytest`, `Flask`, or `Swagger Validator`.







You said:
give me the full updated read me


ChatGPT said:
Here's your fully updated README.md for MyMechanicShop, now including the swagger.yaml API documentation and the automated unit tests you've created:

markdown
Copy
Edit
# 🛠️ MyMechanicShop Backend

**MyMechanicShop** is a RESTful backend API for managing auto repair shops — enabling customers, mechanics, service tickets, and inventory tracking. Built with Flask and SQLAlchemy, it features robust token-based auth, modular architecture, caching, rate limiting, real-time inventory deduction, and now Swagger API documentation with automated tests.

---

## 📁 Project Structure

MyMechanicShop/
│
├── app/
│ ├── blueprints/
│ │ ├── customer/ # Customer routes & schemas
│ │ ├── mechanic/ # Mechanic routes & schemas
│ │ ├── service_ticket/ # Ticket routes, inventory logic, rate limiting
│ │ └── inventory/ # Inventory CRUD with caching
│ ├── utils/ # Token auth, DB init, extensions
│ ├── models.py # SQLAlchemy models + relationships
│ └── init.py # App factory pattern
│
├── tests/ # Automated unit tests for API endpoints
│
├── swagger.yaml # OpenAPI docs for full endpoint specification
├── config.py # Configs (DB URI, secret keys, etc.)
├── run.py # App entry point
├── requirements.txt # Python dependencies
├── .gitignore
└── README.md # You're here!

markdown
Copy
Edit

---

## 🔧 Tech Stack

- Python 3
- Flask (Backend API)
- Flask SQLAlchemy (ORM)
- Marshmallow (Validation/Serialization)
- JWT (Token authentication)
- Flask-Limiter (Rate limiting)
- Flask-Caching (Cached inventory endpoints)
- SQLite (Dev DB — PostgreSQL/MySQL ready)
- Blueprint structure for modular routing
- Swagger (OpenAPI) documentation via `swagger.yaml`
- Pytest + Flask-Testing for unit tests

---

## ✅ Features

### 🔐 Authentication
- JWT-based token auth (`Bearer <token>`)
- Token-protected routes for customer-specific access

### 👤 Customers
- Register, view, update, and delete customers
- Retrieve personal service tickets with token

### 🧑‍🔧 Mechanics
- Add/edit/delete mechanics
- Assign mechanics to service tickets
- Remove mechanics from specific tickets
- List all mechanics assigned to a ticket

### 📝 Service Tickets
- Create new service tickets with mechanic + part associations
- Add/remove inventory parts from a ticket
- Auto-deduct and refund inventory quantities
- Fetch tickets by ID or fetch all
- Retrieve only logged-in customer's tickets
- Rate limiting on sensitive endpoints

### 📦 Inventory
- Full CRUD operations
- Cached GET `/inventory` for performance
- Quantity auto-adjusts when parts are attached to or removed from tickets

---

## 🚀 Running the App

### 1. Install Dependencies
```bash
pip install -r requirements.txt
2. Run the Server
bash
Copy
Edit
python run.py
The app will be live at: http://localhost:5000

📘 API Documentation
A full OpenAPI specification is available via swagger.yaml.

View Swagger Doc
You can use any Swagger viewer (like Swagger Editor):

Import swagger.yaml to view and test all endpoints interactively

🔍 API Overview
Resource	Endpoint	Method	Description
Customers	/customers	GET/POST	List all / Register new customer
/customers/<id>	GET/PUT/DELETE	Retrieve / Update / Delete a customer
Mechanics	/mechanics	GET/POST	List all / Add mechanic
/mechanics/<id>	GET/PUT/DELETE	Retrieve / Update / Delete mechanic
Service Tickets	/tickets	GET/POST	List or create service tickets
/tickets/<id>	GET/PUT/DELETE	Retrieve / Update / Delete ticket
/tickets/my-tickets	GET	Retrieve own service tickets (token required)
/tickets/<id>/mechanics	PUT/GET	Assign/List mechanics for a ticket
/tickets/<id>/mechanics/<id>	DELETE	Remove a mechanic from a ticket
/tickets/<id>/inventory	PUT	Add/remove inventory items from ticket
Inventory	/inventory	GET/POST	List (cached) / Add inventory
/inventory/<id>	GET/PUT/DELETE	Retrieve / Update / Delete inventory

🚧 Rate Limiting (Example)
Endpoint	Limit
PUT /tickets/<id>/mechanics	3/day
PUT /tickets/<id>/inventory	3/day
DELETE /tickets/<id>	5/day

🧪 Automated Tests
📂 tests/ directory includes:
test_customers.py – Tests CRUD + token-restricted ticket retrieval

test_mechanics.py – Tests all mechanic CRUD

test_inventory.py – Tests inventory management + caching

test_service_tickets.py – Tests ticket creation, mechanic/part linking, and inventory adjustment

🧪 Run Tests
bash
Copy
Edit
pytest tests/
Make sure to configure a test database if needed inside config.py

🧠 Future Enhancements
🔐 Admin/User role differentiation

📊 Dashboard metrics (e.g., average repair cost, ticket frequency)

📎 PDF service logs & emailed receipts

🧠 RAG AI assistant to summarize service history

🌐 Public-facing frontend for repair shop clients

👑 Author
PharaohFresh (Donald Clemons)
🎓 Coding Temple Graduate
💻 Software Developer | 🎚️ Audio Engineer
📍 Atlanta, GA
📫 donaldericclemons@gmail.com



