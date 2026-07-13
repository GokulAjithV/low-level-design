The **Open/Closed Principle (OCP)** is the "O" in SOLID. It is the absolute core of building scalable, plug-and-play system architectures.

### 1. The Core Concept

> **"Software entities (classes, modules, functions) should be open for extension, but closed for modification."**

* **Open for Extension:** You should be able to add **new features** or behaviors to your system easily.
* **Closed for Modification:** You should be able to add those new features **without changing a single line of your existing, tested code**.

If you have to open up an existing, working class and edit its internal logic just to add a new feature, you are violating OCP.

---

### 2. Violating OCP (The `if-else` Nightmare)

Let's look at a concrete notification system for your startup. Imagine you start by sending emails, but later your product demands SMS and WhatsApp notifications.

```python
# ❌ VIOLATION OF OCP
class NotificationManager:
    def send_notification(self, target_type, message, recipient):
        # Every time a new channel is added, we MUST modify this file!
        if target_type == "email":
            print(f"Sending Email to {recipient}: {message}")
        elif target_type == "sms":
            print(f"Sending SMS to {recipient}: {message}")
        elif target_type == "whatsapp":
            # Modified later - high risk of introducing bugs to email/sms logic
            print(f"Sending WhatsApp message to {recipient}: {message}")

```

#### Why this breaks down:

1. **Fragility:** Every time you touch this file to add a channel, you risk accidentally breaking the existing email or SMS code.
2. **Merge Conflicts:** If two developers are working on different notification features at the same time, they will both try to modify this exact same block of code.

---

### 3. Refactoring to Comply with OCP

To comply with OCP, we combine **Abstraction** and **Polymorphism**. We close the manager class from modifications by making it depend on an abstract interface.

```python
from abc import ABC, abstractmethod

# 1. Establish the abstract interface (Open for extension)
class NotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient, message):
        pass

# 2. Implement specific extensions
class EmailChannel(NotificationChannel):
    def send(self, recipient, message):
        print(f"Email: {message} sent to {recipient}")

class SMSChannel(NotificationChannel):
    def send(self, recipient, message):
        print(f"SMS: {message} sent to {recipient}")

# 3. The Core Engine: Completely Closed for Modification ✅
class NotificationService:
    def __init__(self, channel: NotificationChannel):
        self.channel = channel

    def execute_delivery(self, recipient, message):
        # This function never changes, no matter how many channels you add
        self.channel.send(recipient, message)

```

#### Adding a New Feature without Touching Existing Code:

If you need to add WhatsApp next week, you don't touch `NotificationService`. You simply plug in a new standalone class:

```python
# New requirement? Just write a new class!
class WhatsAppChannel(NotificationChannel):
    def send(self, recipient, message):
        print(f"WhatsApp: {message} sent to {recipient}")

# Usage
service = NotificationService(WhatsAppChannel())
service.execute_delivery("+91-98765...", "Match is live!")

```

---

### 4. Strategy & Mindset

* **The OCP Indicator:** If you see a long chain of `if-elif-else` or `switch` statements checking for an object's "type," your code is screaming for an OCP refactor using polymorphism.
* **Startup Speed:** By separating concerns this way, you can build new features in isolated files. Your testing overhead drops exponentially because you don't need to re-test old modules when deploying new features.

---

### 5. Action & Accountability

Let’s link this directly to your **Cricket Scoring App** portfolio project.

**Scenario:**
You have a module that calculates the total extra runs given during a match. Right now, it calculates extra runs for **Wides** and **No-Balls**. Tomorrow, you want to add support for **Byes** and **Leg-Byes**.

Following the Open/Closed Principle, how would you design the architecture so that adding new types of extras does *not* require changing your core score calculation engine?