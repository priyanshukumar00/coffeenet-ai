# CoffeeNet (Brewgo)☕

A production-grade Coffee Shop Management System built using FastAPI and MongoDB.

## Features
### Authentication & Authorization
* JWT Authentication
* Role-Based Access Control (RBAC)
* Password Hashing with Passlib & Bcrypt
* Protected Routes

### User Roles
* Admin
* Manager
* Cashier
* Kitchen Staff

### Modules
#### Menu Management
* Create Menu Items
* Update Menu Items
* Delete Menu Items
* View Menu

#### Inventory Management
* Manage Inventory Stock
* Low Stock Monitoring
* Inventory Dashboard
* Quantity Tracking

#### Recipe Management
* Create Recipes
* Map Ingredients to Menu Items
* Recipe Validation

#### Order Management
* Create Orders
* Update Order Status
* Delete Orders
* Automatic Inventory Deduction

#### Dashboard
* Total Products
* Total Orders
* Revenue Summary
* Low Stock Summary

### Security
* JWT Token Authentication
* Role-Based Permissions
* Input Validation using Pydantic
* Environment Variable Management

---

## Tech Stack
### Backend
* FastAPI
* MongoDB Atlas
* Pydantic
* PyMongo
* JWT (python-jose)
* Passlib
* Bcrypt

### Database
* MongoDB Atlas

---
## Roles & Permissions
| Module               | Admin | Manager | Cashier | Kitchen  |
| -------------------- | ----- | ------- | ------- | -------  |
| Menu Management      | ✅     | ❌       | ❌       | ❌     |
| Inventory Management | ✅     | ✅       | ❌       | ❌     |
| Recipe Management    | ✅     | ✅       | ❌       | ❌     |
| Create Orders        | ✅     | ❌       | ✅       | ❌     |
| Update Order Status  | ✅     | ❌       | ❌       | ✅     |
| Dashboard            | ✅     | ✅       | ❌       | ❌     |
| User Management      | ✅     | ❌       | ❌       | ❌     |

---

## Project Status
### Backend
✅ Completed(80%)

