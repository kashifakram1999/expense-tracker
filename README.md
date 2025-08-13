# Expense Tracker System

## Setup Instructions

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
Install dependencies:

bash
pip install -r requirements.txt
Setup environment:

bash
cp .env.example .env
# Edit .env with your actual values
Database setup:

bash
cd src
python manage.py migrate
