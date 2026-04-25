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
