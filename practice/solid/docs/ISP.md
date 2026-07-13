The **Interface Segregation Principle (ISP)** is the "I" in SOLID. It focuses on keeping software systems decoupled, lean, and maintainable.

### 1. The Core Concept

> **"Clients should not be forced to depend on interfaces they do not use."**

In simple terms: Avoid creating massive, "fat" interfaces that try to do everything. Instead, break them down into smaller, highly specific, and focused interfaces.

If a class implements an interface but leaves some methods blank or makes them raise a `NotImplementedError`, your interface is too fat. You are forcing that class to depend on code it doesn't care about.

---

### 2. Violating ISP (The "Fat Interface" Trap)

Let's look at an example from your **Cricket Scoring App**. Imagine you create a single interface for all types of actions a player can perform on a field.

```python
from abc import ABC, abstractmethod

# ❌ VIOLATION OF ISP: Fat Interface
class PlayerActions(ABC):
    @abstractmethod
    def bat(self):
        pass

    @abstractmethod
    def bowl(self):
        pass

    @abstractmethod
    def keep_wickets(self):
        pass

```

#### Why this breaks down:

If you want to create a specialist `Bowler` class, you are forced to implement methods like `keep_wickets()` and `bat()`, even if they don't apply to their primary role in your system logic:

```python
class SpecialistBowler(PlayerActions):
    def bat(self):
        print("Tailender batting defensively.")

    def bowl(self):
        print("Bowling an inswinging yorker.")

    def keep_wickets(self):
        # Forced implementation! This makes no sense for a bowler.
        raise NotImplementedError("Bowlers cannot keep wickets!")

```

This forces your system to handle artificial errors and creates messy dependencies.

---

### 3. Refactoring to Comply with ISP

To fix this, split the giant interface into smaller, role-specific interfaces. In Python, we use multiple inheritance to mix and match these lean interfaces cleanly.

```python
from abc import ABC, abstractmethod

# Lean, segregated interfaces
class Battable(ABC):
    @abstractmethod
    def bat(self):
        pass

class Bowlable(ABC):
    @abstractmethod
    def bowl(self):
        pass

class WicketKeepable(ABC):
    @abstractmethod
    def keep_wickets(self):
        pass

# --- Clean Implementations ---

# A Bowler only implements what they actually do
class SpecialistBowler(Bowlable, Battable):
    def bowl(self):
        print("Bowling at 145 kmph.")
        
    def bat(self):
        print("Batting at position 11.")

# A Wicketkeeper doesn't need to know how to bowl
class WicketKeeper(WicketKeepable, Battable):
    def keep_wickets(self):
        print("Keeping behind the stumps.")
        
    def bat(self):
        print("Opening the innings.")

```

---

### 4. Strategy & Mindset

* **ISP vs LSP:** While Liskov Substitution Principle (LSP) warns you not to *break* parent behavior, ISP stops you from *bloating* your interfaces in the first place.
* **Startup Fit:** By keeping interfaces segregated, your code changes stay localized. If you decide to completely rewrite how wicket-keeping logic works, your `Bowlable` interface and all tracking modules for bowlers remain entirely untouched.

---

### 5. Action & Accountability

You have now covered **4 out of the 5 SOLID principles** (SRP, OCP, LSP, ISP).

Let's test your ability to spot an ISP violation in your SDE tech stack.

**Scenario:**
You are designing a data worker module for your startup. You create a giant abstract class called `DataWorker` with two methods: `read_from_postgres()` and `push_to_elasticsearch()`. You create a specialized class called `LogIndexer` whose only job is to push data into Elasticsearch. It doesn't read from Postgres at all, so you leave `read_from_postgres()` empty.

* **Question:** How would you segregate this interface to adhere to ISP?

Answer this to wrap up your understanding of ISP, and then we will close out SOLID with the final principle: **Dependency Inversion**.