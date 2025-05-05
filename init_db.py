import os
from app import create_app, db
from app.models.user import User

# Remove existing database file if it exists
db_file = 'app.db'
if os.path.exists(db_file):
    os.remove(db_file)
    print(f"Removed existing database file: {db_file}")

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    
    print("Database has been recreated with the new schema.")
    print("You can now run the application with: python run.py") 