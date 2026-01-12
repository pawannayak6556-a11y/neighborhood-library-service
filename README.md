# Neighborhood Library Service

A full-stack library management system built using:

- Python gRPC (backend)
- PostgreSQL (database)
- Node.js (API Gateway)
- React (frontend)

---

## 🏗 Architecture Overview

React UI communicates with a Node.js API Gateway via REST.
The gateway translates requests into gRPC calls handled by a Python service.
All data is persisted in PostgreSQL.

This ensures clean separation of concerns and strong service contracts.

---

## 📦 Features

- Create and list books
- Track available copies
- Borrow books
- Prevent borrowing unavailable books
- End-to-end integration (UI → DB)

---

## 🧰 Tech Stack

| Layer | Technology |
|----|----|
Frontend | React |
API Gateway | Node.js + Express |
Backend | Python + gRPC |
Database | PostgreSQL |
Contracts | Protocol Buffers |

---

## 🚀 Getting Started

### 1️⃣ Clone Repository

```bash
git clone https://github.com/pawannayak6556-a11y/neighborhood-library-service.git
cd neighborhood-library-service
