# 🛠️ MyMechanicShop Backend

This is the backend API for **MyMechanicShop**, a full-stack auto shop management system that allows users to manage customers, mechanics, and service tickets. Built with Flask, this backend provides RESTful endpoints for CRUD operations across multiple entities.

---

## 📁 Project Structure


MyMechanicShop/
│
├── app/
│ ├── blueprints/
│ │ ├── customer/ # Routes and schemas for customer endpoints
│ │ ├── mechanic/ # Routes and schemas for mechanic endpoints
│ │ └── service_ticket/ # Routes and schemas for service ticket management
│ ├── utils/ # Utility functions and app extensions (e.g., DB setup)
│ ├── models.py # SQLAlchemy models for all entities
│ └── init.py # App factory setup
│
├── config.py # App configuration (e.g., DB URI, secret keys)
├── run.py # App entry point
├── requirements.txt # Python package dependencies
├── .gitignore
└── README.md # You’re reading it!



---

## 🔧 Tech Stack

- **Python 3**
- **Flask**
- **Flask SQLAlchemy**
- **Marshmallow** (for serialization)
- **SQLite** (or replace with PostgreSQL/MySQL)
- **Flask Blueprints** for modular architecture

---

## 📦 Features So Far

- ✅ Customer CRUD: create, retrieve, update, delete customer records
- ✅ Mechanic CRUD: manage shop mechanics and their details
- ✅ Service Tickets:
  - Create service tickets linked to customers and mechanics
  - Retrieve ticket information and related records
- ✅ Modular Flask app using Blueprints
- ✅ Schemas for request/response validation using Marshmallow
- ✅ Organized utilities and database initialization

---

## 🚀 Running the App

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt

python run.py

| Resource        | Endpoint          | Method         | Description              |
| --------------- | ----------------- | -------------- | ------------------------ |
| Customers       | `/customers`      | GET/POST       | List all / Add new       |
|                 | `/customers/<id>` | GET/PUT/DELETE | View, update, or delete  |
| Mechanics       | `/mechanics`      | GET/POST       | List all / Add new       |
|                 | `/mechanics/<id>` | GET/PUT/DELETE | View, update, or delete  |
| Service Tickets | `/tickets`        | GET/POST       | List all / Create new    |
|                 | `/tickets/<id>`   | GET/PUT/DELETE | Manage individual ticket |


 Future Plans
 JWT-based authentication

 Admin/user roles

 Dashboard analytics (total tickets, average repair cost, etc.)

 RAG-based assistant for summarizing service logs

👑 Author
PharaohFresh (Donald Clemons)
Coding Temple Grad | Software Dev | Audio Engineer
📍 Atlanta, GA
📫 donaldericclemons@gmail.com

pgsql
Copy
Edit

