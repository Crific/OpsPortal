# Operations Request Portal

##  Overview
Developed a full-stack operations request portal enabling internal task management with role-based access, request assignment, status tracking, and dashboard reporting using Flask, Python, and SQL.

---

##  Project Goal
Build a web application where:
- Users can submit and track requests
- Operators/Admins can manage and update requests
- The system reflects a real internal operations workflow

---

##  Core Features (MVP)
- [ ] User registration and login/logout  
- [ ] Session-based authentication  
- [ ] Create request (ticket)  
- [ ] View user-specific requests  
- [ ] Edit request  
- [ ] Delete request  
- [ ] Status tracking (Pending, In Progress, Resolved)  
- [ ] Protected dashboard page  

---

##  Stretch Features (Optional)
- [ ] Role-based access (Admin, Operator, Viewer)  
- [ ] Request assignment  
- [ ] Priority levels  
- [ ] Dashboard summary (counts by status)  
- [ ] Search and filters  

---

##  Tech Stack
- Backend: Flask (Python)  
- Database: SQLite (SQLAlchemy)  
- Frontend: HTML, CSS  
- Authentication: Sessions + password hashing  

---

##  Data Models

### User
- id  
- username  
- email  
- password_hash  
- role  

### Request
- id  
- title  
- description  
- status  
- priority  
- created_by  
- assigned_to (optional)  
- created_at  

---

## Development Plan

### 1
- [x] Set up database (SQLAlchemy)
- [x] Create User model
- [x] Create Request model
- [x] Run `db.create_all()`

### 2
- [x] Build registration
- [x] Build login/logout
- [x] Implement sessions
- [x] Protect routes

### 3
- [ ] Create request (form → DB)
- [ ] Display requests
- [ ] Edit + delete requests

### 4
- [ ] Add status updates
- [ ] Improve UI
- [ ] Fix bugs

### 5
- [ ] Final polish
- [ ] Clean code
- [ ] Prepare for portfolio

---

##  Key Concepts Demonstrated
- Authentication and session management  
- CRUD operations  
- Relational database design  
- Role-based access (if implemented)  
- Workflow/state management  

##  Future Features

- Admin approval workflow for role upgrades
- Role request system (user → admin approval)
- Email notifications for request updates
- Dashboard analytics (request trends, load, etc.)

---

## ▶️ How to Run

```bash
git clone <your-repo-link>
cd OpsPortal
pip install -r requirements.txt
python app.py