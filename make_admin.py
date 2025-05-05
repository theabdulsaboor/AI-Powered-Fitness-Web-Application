from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Get the user by username
    username = input("Enter the username to make admin: ")
    user = User.query.filter_by(username=username).first()
    
    if user:
        user.is_admin = True
        db.session.commit()
        print(f"User {username} is now an admin!")
    else:
        print(f"User {username} not found!") 