# 🎓 Student Learning Hub

A premium, all-in-one productivity platform designed for modern students. The **Student Learning Hub** centralizes study tools, research capabilities, and task management into a single, high-performance command center.

🚀 **Live Demo:** [https://mini-project-7y8v.onrender.com/](https://mini-project-7y8v.onrender.com/)

---

## ✨ Key Features

### 📚 Study Tools
*   **Notes Management**: Create, edit, and organize your study notes. (Export to PDF coming soon).
*   **Flashcards**: Create and study subject-specific flashcards for better retention.
*   **Focus Timer**: Built-in Pomodoro-style timer to maintain deep work sessions.
*   **Whiteboard**: Digital canvas for sketching ideas and solving problems.

### 🔍 Research & Resources
*   **YouTube Search**: Search for educational videos without leaving the dashboard.
*   **Google Books API**: Find relevant textbooks and reference materials instantly.
*   **Integrated Wikipedia**: Quick research with summaries and direct links.
*   **Smart Dictionary**: Word lookups with phonetics, definitions, and audio pronunciations.

### 📈 Task & Progress Tracking
*   **Homework Tracker**: Manage assignments, deadlines, and completion status.
*   **Interactive Todo List**: Daily task management with progress indicators.
*   **Grades & Analytics**: Track your academic performance with visualized data using Chart.js.
*   **Exam Scheduler**: Keep track of upcoming exams and their importance levels.
*   **Timetable**: Organize your weekly class schedule in a clean, readable format.

### 🤖 AI Assistance (Beta)
*   **AI Assistant**: Generate summaries and quizzes from your study material to test your knowledge.

---

## 🛠️ Technology Stack

*   **Framework**: [Django](https://www.djangoproject.com/) (Python-based Web Framework)
*   **Database**: PostgreSQL (Production on Render) / SQLite (Local Development)
*   **Frontend**: HTML5, CSS3, JavaScript
*   **Styling**: Bootstrap 4 & Django Crispy Forms
*   **Deployment**: Render.com
*   **Static Files**: WhiteNoise (Optimized for production)

---

## 🚀 Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kumar-s29/Mini_Project.git
   cd Mini_Project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python django/studentlearninghub/manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python django/studentlearninghub/manage.py runserver
   ```

---

## 🌐 Deployment

This project is optimized for deployment on **Render**. It uses a `Procfile` for Gunicorn and is pre-configured to use environment variables for security.

### Environment Variables Required:
*   `SECRET_KEY`: Your Django secret key.
*   `DEBUG`: Set to `False` in production.
*   `DATABASE_URL`: Your PostgreSQL connection string.
*   `PYTHON_VERSION`: `3.12.2`

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
