[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23278359&assignment_repo_type=AssignmentRepo)

# 🏨 The Deltin Hotel — Polyglot Persistence Application
### BEMM459 Database Technologies for Business Analytics
**University of Exeter Business School | Group Assignment | March 2026**

---

## 📋 Project Overview

This project implements a **Polyglot Persistence** database application for **The Deltin**, a fictitious mid-to-upscale UK hotel chain. The application combines two database technologies to manage different categories of hotel data:

- **Microsoft SQL Server** — manages structured, transactional data (guests, rooms, bookings, payments, staff)
- **MongoDB** — manages semi-structured enrichment data (guest preferences, post-stay reviews)

The two systems are integrated via a **Python pipeline** that assembles unified guest profiles by querying both databases simultaneously.

---

## 🗂️ Repository Structure

```
📁 SQL/
    DDL.sql          — Creates all 5 tables with constraints
    DML.sql          — Inserts sample data and SELECT queries

📁 NoSQL/
    hotel_nosql.py   — MongoDB operations (insert & retrieve)
    pipeline.py      — Connects SQL Server + MongoDB together

📁 ER diagram/
    ERD_Diagram.pdf          — Entity-Relationship Diagram


README.md            — This file
```

---

## 🗄️ SQL Server Component

**Server:** `mcruebs04.isad.isadroot.ex.ac.uk`

### Tables Created (DDL.sql)

| Table | Primary Key | Description |
|---|---|---|
| Guest | GuestID | Stores guest personal details |
| Room | RoomID | Stores room inventory and pricing |
| Booking | BookingID | Links guests to rooms with dates |
| Payment | PaymentID | Records payment per booking |
| Staff | StaffID | Stores employee information |

### Key Relationships
- `Guest` → `Booking` : One-to-many
- `Room` → `Booking` : One-to-many
- `Booking` → `Payment` : One-to-one
- `Booking` → `Staff` : Many-to-one

### Sample Queries (DML.sql)
- Retrieve all bookings for a specific guest
- Calculate total revenue by room type
- Identify rooms with highest occupancy

---

## 🍃 MongoDB Component

**Host:** `localhost:27017`
