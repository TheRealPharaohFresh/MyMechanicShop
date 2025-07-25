# 🛠️ MyMechanicShop Backend

**MyMechanicShop** is a RESTful backend API for managing auto repair shops — enabling customers, mechanics, service tickets, and inventory tracking. Built with Flask and SQLAlchemy, it features robust token-based auth, modular architecture, caching, rate limiting, and real-time inventory deduction.

---

## 📁 Project Structure

```
MyMechanicShop/
│
├── app/
│   ├── blueprints/
│   │   ├── customer/           # Customer routes & schemas
│   │   ├── mechanic/           # Mechanic routes & schemas
│   │   ├── service_ticket/     # Ticket routes, inventory logic, rate limiting
│   │   └── inventory/          # Inventory CRUD with caching
│   ├── utils/                  # Token auth, DB init, extensions
│   ├── models.py               # SQLAlchemy models + relationships
│   └── __init__.py             # App factory pattern
│
├── config.py                   # Configs (DB URI, secret keys, etc.)
├── run.py                      # App entry point
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md                   # You're here!
```

---

## 🔧 Tech Stack

* **Python 3**
* **Flask** (Backend API)
* **Flask SQLAlchemy** (ORM)
* **Marshmallow** (Validation/Serialization)
* **JWT** (Token authentication)
* **Flask-Limiter** (Rate limiting)
* **Flask-Caching** (Cached inventory endpoints)
* **SQLite** (Dev DB — PostgreSQL/MySQL ready)
* **Blueprints** for modular routing

---

## ✅ Features

### 🔐 Authentication

* JWT-based token auth (`Bearer <token>`)
* Token-protected routes for customer-specific access

### 👤 Customers

* Register, view, update, and delete customers
* Retrieve own service tickets via token

### 🧑‍🔧 Mechanics

* Add/edit/delete mechanics
* Assign mechanics to service tickets
* Remove mechanics from specific tickets
* List all mechanics assigned to a ticket

### 📝 Service Tickets

* Create new service tickets with mechanic + part associations
* Add/remove inventory parts from a ticket
* Auto-deduct and refund inventory quantities
* Get tickets by ID or fetch all
* Fetch tickets only for logged-in customer
* Rate limiting on sensitive endpoints

### 📦 Inventory

* Full CRUD: add, get, update, delete
* Cached GET requests (`/inventory`) for performance
* Quantity auto-adjusted when attached to tickets

---

## 🚀 Running the App

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python run.py
```

App will launch at: `http://localhost:5000`

---

## 🔁 API Overview

| Resource        | Endpoint                       | Method         | Description                             |
| --------------- | ------------------------------ | -------------- | --------------------------------------- |
| Customers       | `/customers`                   | GET/POST       | List all / Register new customer        |
|                 | `/customers/<id>`              | GET/PUT/DELETE | Get, update, or delete a customer       |
| Mechanics       | `/mechanics`                   | GET/POST       | List all / Add new mechanic             |
|                 | `/mechanics/<id>`              | GET/PUT/DELETE | Get, update, or delete a mechanic       |
| Service Tickets | `/tickets`                     | GET/POST       | List or create service tickets          |
|                 | `/tickets/<id>`                | GET/PUT/DELETE | Get, update, or delete ticket           |
|                 | `/tickets/my-tickets`          | GET            | Get logged-in customer's tickets        |
|                 | `/tickets/<id>/mechanics`      | PUT/GET        | Bulk update / get mechanics on a ticket |
|                 | `/tickets/<id>/mechanics/<id>` | DELETE         | Remove a specific mechanic              |
|                 | `/tickets/<id>/inventory`      | PUT            | Add/remove inventory parts on a ticket  |
| Inventory       | `/inventory`                   | GET/POST       | List (cached) / Add inventory           |
|                 | `/inventory/<id>`              | GET/PUT/DELETE | Retrieve / Update / Delete inventory    |

---

## 🚧 Rate Limiting (Example Limits)

* `PUT /tickets/<id>/mechanics`: 3 per day
* `PUT /tickets/<id>/inventory`: 3 per day
* `DELETE /tickets/<id>`: 5 per day

---

## 🧠 Future Enhancements

* ✅ **JWT Auth** (done)
* 🧪 Add unit + integration tests
* 🔐 Admin/User role differentiation
* 📊 Dashboard metrics (average repair cost, revenue)
* 🧠 AI Assistant using RAG to summarize service history
* 🧾 Email receipts or PDF service logs

---

## 👑 Author

**PharaohFresh (Donald Clemons)**
🎓 Coding Temple Graduate
💻 Software Developer | 🎚️ Audio Engineer
📍 Atlanta, GA
📫 [donaldericclemons@gmail.com](mailto:donaldericclemons@gmail.com)




