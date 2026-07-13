The **Single Responsibility Principle (SRP)** is the first principle of SOLID design.

### 1. The Core Concept

> **"A class should have one, and only one, reason to change."** — Robert C. Martin

SRP is not about making your classes have only one *method*; it means a class should focus on **one single actor or business function**. If a class has to change because the database team changes their schema *and* because the finance team changes how taxes are calculated, that class has **two** responsibilities. It is tightly coupled and fragile.

---

### 2. Violating SRP (The "God Class" Trap)

Let's look at a scenario from a **Cricket Scoring Application**. Imagine a class that handles user profile management, database operations, and notifications all at once.

```python
# ❌ VIOLATION OF SRP
class UserProfile:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_profile_data(self):
        return {"username": self.username, "email": self.email}

    def save_to_database(self):
        # Complex connection logic to Postgres/Supabase
        print(f"Saving {self.username} to production database...")

    def send_welcome_email(self):
        # Complex SMTP connection and HTML email formatting
        print(f"Sending email to {self.email}...")

```

#### Why this is dangerous:

1. **Multiple Reasons to Change:** If you switch your database from Postgres to MongoDB, you must edit this class. If you switch your email provider from SendGrid to AWS SES, you must edit this *same* class.
2. **Testing Overhead:** Testing user profile properties requires mocking out database networks and email servers.

---

### 3. Refactoring to SRP (The Decoupled Way)

To fix this, we break the class apart based on **responsibility zones**. Each class becomes an expert in exactly one job.

```python
# 1. Responsibility: Manage User Data Structure
class UserProfile:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_profile_data(self):
        return {"username": self.username, "email": self.email}


# 2. Responsibility: Handle Database Operations (Data Persistence)
class UserRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def save(self, user: UserProfile):
        print(f"Database: Saving {user.username} successfully.")


# 3. Responsibility: Handle Communications (Notifications)
class NotificationService:
    def send_welcome_email(self, user: UserProfile):
        print(f"Notification: Email sent to {user.email}.")

```

#### How they execute cleanly together:

```python
# Orchestration (e.g., in a controller or manager function)
new_user = UserProfile("gokul_ajith", "gokul@example.com")

# Pass the object to the specialized services
db_manager = UserRepository(db_client="postgres_pool")
email_manager = NotificationService()

db_manager.save(new_user)
email_manager.send_welcome_email(new_user)

```

---

### 4. Strategy & Mindset

* **High Cohesion:** When you apply SRP, your classes become highly cohesive. Everything inside `UserRepository` is strictly related to data storage.
* **Startup Velocity:** If your email service crashes or needs an update, you rewrite `NotificationService`. Your core business logic (`UserProfile`) and database logic (`UserRepository`) remain completely untouched. You drastically minimize the risk of regression bugs.

---

### 5. Action & Accountability

Let's see if you can spot the boundary line in your own domain.

**Scenario:**
You have a `MatchScorer` class in your cricket app. It tracks the current runs, wickets, and overs. You want to add a feature where, at the end of the match, it generates a text-based "Match Summary Report" file and saves it to the local disk.

**Your Task:**
Should the code that formats the text and writes the file to the disk live inside the `MatchScorer` class, or should it live somewhere else? Why?