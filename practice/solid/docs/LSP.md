The **Liskov Substitution Principle (LSP)** states: *"Objects of a subclass should be replaceable with objects of the parent class without breaking the program."*  In plain terms — if your code works with a parent class, it must work equally well with any child class. [tusharghosh09006.medium](https://tusharghosh09006.medium.com/liskov-substitution-principle-lsp-744eceb29e8)

***

## The Real-World Anchor

Think of a **power socket**. Any plug that fits the socket should work correctly — a phone charger, a laptop charger, a fan. If one plug fits the socket but causes a short circuit, it's violating the "socket contract". LSP says: child classes must honor the parent's contract fully. [youtube](https://www.youtube.com/watch?v=WDxh-OfsdPo)

***

## ❌ Violating LSP — The Classic Example

```python
class Bird:
    def fly(self):
        print("Flying!")

class Sparrow(Bird):
    def fly(self):
        print("Sparrow flying!")

class Ostrich(Bird):        # ❌ Ostrich CAN'T fly!
    def fly(self):
        raise Exception("Ostriches can't fly!")  # Breaks the contract

# This breaks when Ostrich is substituted
def make_bird_fly(bird: Bird):
    bird.fly()              # Works for Sparrow, CRASHES for Ostrich

make_bird_fly(Sparrow())    # ✅ Fine
make_bird_fly(Ostrich())    # ❌ Exception — LSP violated
```

`Ostrich` inherits `Bird` but *can't honor* the `fly()` contract. Substituting it breaks the program. [tusharghosh09006.medium](https://tusharghosh09006.medium.com/liskov-substitution-principle-lsp-744eceb29e8)

***

## ✅ Fixing LSP — Restructure the Hierarchy

The fix is to **not force a subclass into a contract it can't fulfill**. Split the hierarchy based on actual capabilities. [blog.logrocket](https://blog.logrocket.com/liskov-substitution-principle-lsp/)

```python
class Bird:
    def eat(self):
        print("Eating...")

class FlyingBird(Bird):         # Only birds that CAN fly
    def fly(self):
        print("Flying!")

class Sparrow(FlyingBird):
    def fly(self):
        print("Sparrow flying!")

class Ostrich(Bird):            # ✅ Doesn't inherit fly() — honest contract
    def run(self):
        print("Ostrich running!")

def make_bird_fly(bird: FlyingBird):
    bird.fly()                  # Only called on flying birds — safe!

make_bird_fly(Sparrow())        # ✅ Works perfectly
```

Now `Ostrich` is still a `Bird`, but it never promises to fly. No contract broken. [blog.logrocket](https://blog.logrocket.com/liskov-substitution-principle-lsp/)

***

## Another Practical Example — Payment System

```python
class Payment:
    def pay(self, amount):
        pass
    
    def refund(self, amount):
        pass

class CreditCardPayment(Payment):
    def pay(self, amount):
        print(f"Credit card: ₹{amount}")
    
    def refund(self, amount):
        print(f"Refunding ₹{amount} to card")

class CryptoPayment(Payment):
    def pay(self, amount):
        print(f"Crypto: ₹{amount}")
    
    def refund(self, amount):
        raise Exception("Crypto is non-refundable!")  # ❌ LSP violated!
```

`CryptoPayment` can't honor `refund()`. Fix: create a separate `RefundablePayment` abstract class, and only make `CreditCardPayment` extend it.  `CryptoPayment` extends `Payment` only. [tusharghosh09006.medium](https://tusharghosh09006.medium.com/liskov-substitution-principle-lsp-744eceb29e8)

***

## The Quick Violation Checklist

You're violating LSP if a child class: [blog.logrocket](https://blog.logrocket.com/liskov-substitution-principle-lsp/)

- Throws an exception for a method the parent supports
- Returns a completely different type than expected
- Does *nothing* (empty `pass`) for a method the parent defines as meaningful
- Has stricter input validation than the parent

***

## LSP + Polymorphism Connection

LSP is what makes **polymorphism safe**.  When you loop through a list of `Payment` objects and call `.pay()`, LSP guarantees every subclass behaves correctly — no surprises, no crashes. Without LSP, polymorphism is a ticking time bomb. [youtube](https://www.youtube.com/watch?v=WDxh-OfsdPo)

***

## SOLID Progress Tracker

| Principle | Status |
|-----------|--------|
| **S** — Single Responsibility | ✅ Done |
| **O** — Open/Closed | ⏳ Pending |
| **L** — Liskov Substitution | ✅ Done (today) |
| **I** — Interface Segregation | ⏳ |
| **D** — Dependency Inversion | ⏳ |

***

## Practice Task Right Now

Find the LSP violation here and fix it:

```python
class Shape:
    def area(self): pass
    def volume(self): pass   # 3D concept

class Circle(Shape):
    def area(self): return 3.14 * 5 * 5
    def volume(self): raise Exception("2D shape has no volume!")
```

How would you restructure this hierarchy so no class is forced to implement a method it can't honor? Solve this — it's a common LLD interview question. 💪