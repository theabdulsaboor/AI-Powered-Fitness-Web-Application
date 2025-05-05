from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    users = User.query.all()
    if users:
        print("\nExisting users:")
        for user in users:
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Admin: {user.is_admin}")
            print("-" * 30)
    else:
        print("No users found in the database.") 