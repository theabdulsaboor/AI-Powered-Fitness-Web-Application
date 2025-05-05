# AI-Powered Fitness Web App

A Flask-based web application that generates personalized workout plans using AI (Decision Tree) based on user's fitness data.

## Features

- User Authentication (Register/Login)
- AI-Powered Workout Plan Generation
- Personalized Dashboard
- Admin Panel with SQL Console
- Modern Dark Theme UI
- Responsive Design

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

4. Run the application:
```bash
flask run
```

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── instance/
├── migrations/
├── .env
├── config.py
└── run.py
```

## Technologies Used

- Flask
- SQLite
- scikit-learn (Decision Tree)
- Bootstrap 5
- Flask-SQLAlchemy
- Flask-Login 