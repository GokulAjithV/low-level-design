# Violating SRP (The "God Class" Trap)

class UserProfile:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_user_details(self):
        return {"username": self.username, "email": self.email}

    def save_to_database(self):
        # complex connection logic to postgres
        print(f"Saving {self.username} to database")

    def send_welcome_email(self):
        # complex SMTP connection and HTML email formatting
        print(f"Sending email to {self.email}...")

# Refactoring to SRP (The Decoupled Way)

class UserProfile:

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_user_detail(self):
        return {"username" : self.username, "email": self.email}

class UserRepository:

    def __init__(self, db_client):
        self.db_client = db_client

    def save(self, user: UserProfile):
        print(f"Database: Saving {user.username} details successfully")

class NotificationService:

    def send_welcome_email(self, user: UserProfile):
        print(f"Notification: Email sent to {user.email}")


new_user = UserProfile("gokul_ajith", "gokul@gmail.com")

db_manager = UserRepository("postgres_pool")
email_manager = NotificationService()

db_manager.save(new_user)
email_manager.send_welcome_email(new_user)

