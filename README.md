# 🚀 Task Flow - Modern Task Management System

A full-stack task management system for planning, tracking, and managing software projects. The platform enables teams to create boards, manage sprints, track issues, assign tasks, and monitor workflows through a modern web interface.

![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![MySQL](https://img.shields.io/badge/MySQL-8+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.x-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

---

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🔐 **Authentication & Authorization**
- JWT-based secure authentication
- Role-based access control (Admin, Manager, Developer)
- Token refresh mechanism
- Session management

### 📊 **Board Management**
- **Scrum Boards** - Sprint-based development (TODO → IN_PROGRESS → REVIEW → DONE)
- **Kanban Boards** - Continuous flow (TODO → IN_PROGRESS → DONE)
- Drag-and-drop card management
- Custom column creation

### 📋 **Backlog & Issue Tracking**
- Create, update, and delete issues/tasks
- Priority levels (High, Medium, Low)
- Issue types (Task, Bug, Story)
- Search and filter capabilities
- Move issues to boards and sprints

### 🏃 **Sprint Planning**
- Create and manage sprints
- Visual progress tracking
- Start/Complete sprints
- Sprint goal setting
- Date-based tracking

### 🤖 **AI Assistant**
- Smart context-aware responses
- Project overview and analytics
- Task recommendations
- Deadline insights
- Natural language queries

### 🔔 **Notifications**
- Real-time notifications
- Mark as read/unread
- Bulk delete
- Type-based filtering

### 👤 **User Management**
- Profile management
- Role-based permissions
- Account settings

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Django** | 5.0 | Python web framework |
| **Django REST Framework** | 3.15 | API development |
| **PyJWT** | 2.8 | JWT authentication |
| **MySQL** | 8+ | Production database |
| **django-cors-headers** | 4.3 | CORS handling |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18+ | UI library |
| **Tailwind CSS** | 3.x | Styling |
| **React Router DOM** | 6.x | Navigation |
| **Axios** | 1.x | HTTP client |
| **React Icons** | 5.x | Icon library |
| **React Toastify** | 10.x | Notifications |
| **@hello-pangea/dnd** | 16.x | Drag & drop |
| **React Markdown** | 9.x | Markdown rendering |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

| Software | Version | Download |
|----------|---------|----------|
| **Python** | 3.11+ | [Download](https://www.python.org/downloads/) |
| **Node.js** | 18+ | [Download](https://nodejs.org/) |
| **MySQL** | 8+ | [Download](https://dev.mysql.com/downloads/) |
| **Git** | Latest | [Download](https://git-scm.com/) |

### Verify Installations
```bash
# Check Python version
python --version

# Check Node.js version
node --version

# Check npm version
npm --version

# Check MySQL version
mysql --version

## 🚀 Installation
### Step 1: Clone the Repository
```git clone https://github.com/yourusername/task-management-system.git
cd task-management-system
```
### Step 2: Backend Setup
``` python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```
### Step 3: Frontend Setup
### 3.1 Navigate to Frontend Directory
```
cd frontend
```
### 3.2 Install Node Dependencies
```
npm install
```
### Step 4: MySQL Setup
#### 4.1 Start MySQL Service
```
# Windows
net start MySQL

# macOS
brew services start mysql

# Linux
sudo systemctl start mysql
```
### 4.2 Verify MySQL is Running
```
mysql --version
```
## ⚙️ Configuration
### Backend Configuration
Create an application.properties file in:
```
cd backend/src/main/resources
```
Edit application.properties with the following content:

```
# MySQL Configuration
# MySQL Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'taskManagement',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```
### Frontend Configuration
Create a .env file in the frontend/ directory:
```
cd frontend
```
Create frontend/.env file with the following content:
# API Base URL
REACT_APP_API_URL=http://127.0.0.1:8000

## 🏃 Running the Application
### Step 1: Start MySQL

Make sure MySQL service is running (see MySQL Setup section)
### Step 2: Start Backend Server
```# Navigate to backend directory
cd backend

# Navigate to project root directory
cd task-flow

# Start Django server
python manage.py runserver
```
### Step 3: Start Frontend Development Server
Open a new terminal and run:
```
# Navigate to frontend directory
cd frontend

# Start React development server
npm start
```
Frontend will be available at:
http://localhost:3000 


