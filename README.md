# Approval Workflow App (Flask)

This is a role-based approval workflow system built using Flask.

The idea behind this project was to understand how real-world systems handle
user roles, authentication, and approval flows instead of just basic CRUD apps.

## Features
- User authentication (Signup / Login / Logout)
- Role-based access (User & Admin)
- Users can submit requests
- Admin can approve or reject requests
- Secure session handling
- Clean folder structure following Flask best practices

## Tech Stack
- Python
- Flask
- Flask-Login
- Flask-WTF
- SQLAlchemy
- SQLite
- HTML, CSS

## What I Learned
- How authentication works in backend systems
- Role-based authorization (admin vs user)
- Database relationships using SQLAlchemy
- Structuring Flask apps for real projects
- Using Git and GitHub for version control

## How to Run Locally
```bash
git clone https://github.com/bhavshx-collab/approval-workflow-app.git
cd approval-workflow-app
pip install -r requirements.txt
python app.py
