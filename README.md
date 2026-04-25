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

## 📁 Project Structure
```
task-flow/
│
├── 📁 backend/                          # Django Backend
│   ├── 📁 task_management/              # Main Django Project
│   │   ├── __init__.py
│   │   ├── settings.py                  # ⚙️ Main Configuration
│   │   ├── urls.py                      # 🌐 Main URL Routing
│   │   ├── asgi.py                      # ASGI Configuration
│   │   └── wsgi.py                      # 🚀 WSGI Configuration
│   │
│   ├── 📁 users/                        # 👤 User Management
│   │   ├── 📁 migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── models.py                    # 🗃️ User Model
│   │   ├── views.py                     # 🔐 Auth Views (Login/Register/Profile)
│   │   ├── urls.py                      # 🌐 Auth Routes
│   │   ├── serializers.py               # 📦 User Serializers
│   │   └── authentication.py            # 🔑 JWT Authentication
│   │
│   ├── 📁 boards/                       # 📊 Board Management
│   │   ├── 📁 migrations/
│   │   ├── __init__.py
│   │   ├── models.py                    # 🗃️ Board Model (Scrum/Kanban)
│   │   ├── views.py                     # 🎯 Board Operations
│   │   ├── urls.py                      # 🌐 Board Routes
│   │   └── serializers.py               # 📦 Board Serializers
│   │
│   ├── 📁 issues/                       # 🐛 Issue/Backlog Management
│   │   ├── 📁 migrations/
│   │   ├── __init__.py
│   │   ├── models.py                    # 🗃️ Issue & Comment Models
│   │   ├── views.py                     # 📋 Backlog & Issue Operations
│   │   ├── urls.py                      # 🌐 Issue Routes
│   │   └── serializers.py               # 📦 Issue Serializers
│   │
│   ├── 📁 sprints/                      # 🏃 Sprint Management
│   │   ├── 📁 migrations/
│   │   ├── __init__.py
│   │   ├── models.py                    # 🗃️ Sprint Model
│   │   ├── views.py                     # 🏃 Sprint Operations
│   │   ├── urls.py                      # 🌐 Sprint Routes
│   │   └── serializers.py               # 📦 Sprint Serializers
│   │
│   ├── 📁 notifications/                # 🔔 Notifications
│   │   ├── 📁 migrations/
│   │   ├── __init__.py
│   │   ├── models.py                    # 🗃️ Notification Model
│   │   ├── views.py                     # 🔔 Notification Operations
│   │   └── urls.py                      # 🌐 Notification Routes
│   │
│   ├── 📁 ai/                           # 🤖 AI Assistant
│   │   ├── 📁 migrations/
│   │   ├── __init__.py
│   │   ├── views.py                     # 🧠 Smart AI Responses
│   │   └── urls.py                      # 🌐 AI Routes
│   │
│   ├── 📁 templates/                    # 🖼️ Django Templates
│   │
│   ├── manage.py                        # 🚀 Django Management Script
│   └── requirements.txt                 # 📦 Python Dependencies
│
├── 📁 frontend/                         # ⚛️ React Frontend
│   ├── 📁 public/
│   │   └── index.html                   # 🖼️ Main HTML File
│   │
│   ├── 📁 src/
│   │   ├── 📁 api/
│   │   │   └── axios.js                 # 🌐 HTTP Client Setup
│   │   │
│   │   ├── 📁 components/
│   │   │   ├── Layout.jsx               # 🧭 Main Layout (Sidebar + Header)
│   │   │   └── ProtectedRoute.jsx       # 🔐 Route Protection
│   │   │
│   │   ├── 📁 pages/
│   │   │   ├── LoginPage.jsx            # 🔑 Login Interface
│   │   │   ├── RegisterPage.jsx         # 📝 Registration Interface
│   │   │   ├── Dashboard.jsx            # 📊 Main Dashboard
│   │   │   ├── BoardsPage.jsx           # 🎯 Board Management
│   │   │   ├── BoardView.jsx            # 👁️ Board Detail View
│   │   │   ├── CreateBoard.jsx          # ✨ Create New Board
│   │   │   ├── BacklogPage.jsx          # 📋 Backlog Management
│   │   │   ├── SprintPage.jsx           # 🏃 Sprint Planning
│   │   │   ├── AIChatPage.jsx           # 🤖 AI Assistant
│   │   │   ├── NotificationsPage.jsx    # 🔔 Notifications Center
│   │   │   └── ProfilePage.jsx          # 👤 User Profile
│   │   │
│   │   ├── 📁 utils/
│   │   │   └── permissions.js           # 🔐 Permission Helpers
│   │   │
│   │   ├── App.js                       # ⚛️ Main Application Component
│   │   ├── App.css                      # 🎨 App Styles
│   │   ├── index.js                     # 🎬 Application Entry Point
│   │   ├── index.css                    # 🌍 Global Styles
│   │   ├── logo.svg                     # 🖼️ Logo Asset
│   │   ├── reportWebVitals.js           # 📊 Performance Metrics
│   │   └── setupTests.js                # 🧪 Test Setup
│   │
│   ├── .gitignore                       # 🙈 Git Ignore Rules
│   ├── package.json                     # 📦 Frontend Dependencies
│   ├── package-lock.json                # 🔒 Lockfile
│   ├── README.md                        # 📖 Frontend Documentation
│   └── tailwind.config.js               # 🎨 Tailwind CSS Config
│
├── .gitignore                           # 🙈 Main Git Ignore
└── README.md                            # 📖 Main Documentation
```

## 📖 Usage Guide

### 1. Register & Login
- Open the application at `http://localhost:3000`
- Click **Register** to create a new account
- Enter username, email, password, and select role
- Login using your credentials

### 2. Create a Board
- Navigate to **Boards** page from sidebar
- Click **Create Board** button
- Enter board name and select board type:
  - **Scrum** - Sprint-based development (TODO → IN_PROGRESS → REVIEW → DONE)
  - **Kanban** - Continuous workflow (TODO → IN_PROGRESS → DONE)
- Click **Create** to save

### 3. Create Issues / Tasks
- Navigate to **Backlog** page
- Click **Create Issue** button
- Enter title, description, select type (Task/Bug/Story)
- Select priority (High/Medium/Low)
- Click **Create Issue** to save to backlog

### 4. Move Issues to Board
- In Backlog page, click **Move to Board** on any issue
- Select a board from the dropdown
- Issue will appear on the selected board in TODO column

### 5. Update Task Status (Drag & Drop)
- Go to **Boards** page and select a board
- Drag and drop cards between columns:
  - **Scrum**: TODO → IN_PROGRESS → REVIEW → DONE
  - **Kanban**: TODO → IN_PROGRESS → DONE
- Status updates automatically

### 6. Create and Manage Sprints (Scrum only)
- Navigate to **Sprints** page
- Click **Create Sprint** button
- Enter sprint name, start date, end date, and goal
- Select a Scrum board
- Click **Create Sprint**
- Click **Start Sprint** when ready

### 7. Track Progress
- View **Dashboard** for project overview
- Check **Sprints** page for sprint progress
- Monitor task statistics on Dashboard:
  - Total boards
  - Backlog items
  - Completed/In progress tasks
  - Active sprints

### 8. Use AI Assistant
- Navigate to **AI Assistant** page
- Ask questions like:
  - "Show me project overview"
  - "How many tasks are pending?"
  - "What's my sprint progress?"
  - "Give me recommendations"
  - "Show my boards"

### 9. Manage Notifications
- Click **Notifications** bell icon
- View all notifications
- Mark as read/unread
- Delete notifications
- Delete multiple notifications (select mode)

### 10. Search & Filter Issues
- In **Backlog** page, use search bar to find issues by title/description
- Filter by priority (High/Medium/Low/All)
- Filter by type (Task/Bug/Story/All)
- Results update automatically

## 📚 API Documentation

#### Authentication

- `POST /api/register/` – Register new user
- `POST /api/login/` – User login (returns JWT token)
- `GET /api/profile/` – Get current user profile
- `PUT /api/profile/update/` – Update user profile

#### Boards

- `GET /api/boards/` – List all boards
- `POST /api/boards/create_board/` – Create new board
- `GET /api/boards/{id}/` – Get board details
- `DELETE /api/boards/{id}/delete/` – Delete board
- `GET /api/boards/{id}/columns/` – Get board columns
- `GET /api/boards/{id}/issues/` – Get issues for a board

#### Backlog & Issues

- `GET /api/issues/backlog/` – Get all backlog issues
- `POST /api/issues/create/` – Create new issue
- `GET /api/issues/{id}/` – Get issue details
- `DELETE /api/issues/{id}/` – Delete issue
- `PATCH /api/issues/{id}/status/` – Update issue status
- `PATCH /api/issues/{id}/move-to-board/` – Move issue to board
- `PATCH /api/issues/{id}/move-to-backlog/` – Move issue back to backlog
- `PATCH /api/issues/{id}/assign-to-sprint/` – Assign issue to sprint

#### Sprints

- `GET /api/sprints/` – List all sprints
- `POST /api/sprints/create/` – Create a new sprint
- `GET /api/sprints/{id}/issues/` – Get issues in a sprint
- `PUT /api/sprints/{id}/start/` – Start a sprint
- `PUT /api/sprints/{id}/close/` – Complete a sprint
- `DELETE /api/sprints/{id}/delete/` – Delete a sprint

#### Notifications

- `GET /api/notifications/` – Get all notifications
- `PUT /api/notifications/{id}/read/` – Mark notification as read
- `PUT /api/notifications/read-all/` – Mark all notifications as read
- `DELETE /api/notifications/{id}/` – Delete a notification

#### AI Assistant

- `POST /api/ai/chat/` – Send message to AI assistant
- `GET /api/ai/suggestions/` – Get suggested questions

#### Board Cards (Drag & Drop)

- `GET /api/boardCard/board/{board_id}/` – Get all cards for a board
- `PUT /api/boardCard/{card_id}/move/{column_id}/` – Move card to a column

#### Date/Time Endpoints

- `GET /api/issues/overdue/` – Get overdue tasks
- `GET /api/issues/upcoming/` – Get tasks due in next 7 days
- `GET /api/issues/by-date/{date}/` – Get tasks for a specific date
- `GET /api/issues/statistics/` – Get date-based task statistics
  
## 🖼️ Screenshots

<div align="center">

### 🔐 Authentication

| Login Page | Registration |
|:---:|:---:|
| <img width="500" alt="Login Page" src="https://github.com/user-attachments/assets/d18bb401-389f-4515-a10a-16373d31b5de" /> | <img width="500" alt="Registration Page" src="https://github.com/user-attachments/assets/82b2e7b4-0cfd-4587-8b10-1b9b51d6fab2" /> |
| *Secure JWT-based login interface* | *User registration with role selection* |

---

### 📊 Dashboard

<img width="800" alt="Dashboard" src="https://github.com/user-attachments/assets/c7f89fa0-00dd-45cf-b972-514d7a51d081" />

*Main dashboard showing project statistics, recent activity, and team overview*

---

### 🎯 Boards

| Create Board | Board View |
|:---:|:---:|
| <img width="400" alt="Create Board" src="https://github.com/user-attachments/assets/26830cfe-14a6-41b0-b061-bf5aff86ebc0" /> | <img width="400" alt="Board View" src="https://github.com/user-attachments/assets/d2d2b3ff-01ef-4d7f-b00d-02a83480efc9" /> |
| *Create new board interface* | *Interactive Kanban board with drag-and-drop* |

---

### 📋 Backlog

<img width="800" alt="Backlog" src="https://github.com/user-attachments/assets/fe6ca6f0-cb9d-48f2-adff-c5a6f1a9b96e" />

*Product backlog with prioritization and issue tracking*

---

### 🏃 Sprints

<img width="800" alt="Sprints" src="https://github.com/user-attachments/assets/56514c2f-c606-495f-bcaf-93148c0e0d6c" />

*Active sprint tracking with progress visualization*

---

### 🤖 AI Assistant

<img width="800" alt="AI Assistant" src="https://github.com/user-attachments/assets/aa6b7da0-6bba-4dc7-9975-75acaefc2614" />

*Smart AI assistant for project insights and recommendations*

---

### 🔔 Notifications

<img width="800" alt="Notifications" src="https://github.com/user-attachments/assets/9c2eff54-bda7-40a1-8aa7-b29a4ba82f00" />

*Real-time notification center with activity feed*

---

### 👤 Profile

<img width="800" alt="Profile" src="https://github.com/user-attachments/assets/6d246357-805b-4f42-a00a-327524bdc8b3" />

*User profile management and settings*

</div>
---

## 📱 Features Showcased

| Feature | Description |
|---------|-------------|
| 🔐 **Authentication** | Secure JWT-based login and registration |
| 📊 **Dashboard** | Project statistics and activity overview |
| 🎯 **Boards** | Scrum & Kanban boards with drag-and-drop |
| 📋 **Backlog** | Issue tracking with priorities and types |
| 🏃 **Sprints** | Sprint planning and progress tracking |
| 🤖 **AI Assistant** | Smart project insights and recommendations |
| 🔔 **Notifications** | Real-time alerts and updates |
| 👤 **Profile** | User profile management |


> 💡 *All screenshots show the actual working interface of the Task Management System with real data and interactions.*

> Made with ❤️ by Ranjan  
⭐ If this project will help you, give a star to this repo
