from abc import ABC, abstractmethod

# =====================================================================
# CHALLENGE: Multi-Layered Notification Service
# =====================================================================

# 1. Define the Component Interface
class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass


# 2. Implement the Concrete Component
class BaseNotifier(Notifier):
    def send(self, message: str) -> str:
        # TODO: Return the original message
        pass


# 3. Implement the Base Decorator
class NotifierDecorator(Notifier, ABC):
    def __init__(self, notifier: Notifier):
        # TODO: Store reference to the wrapped notifier
        pass

    @abstractmethod
    def send(self, message: str) -> str:
        pass


# 4. Implement Concrete Decorators
class EmailDecorator(NotifierDecorator):
    def send(self, message: str) -> str:
        # TODO: Wrap the notifier call, and prefix with "[Email] "
        # Hint: call the wrapped notifier's send() method, then prepend/prepend
        pass


class SMSDecorator(NotifierDecorator):
    def send(self, message: str) -> str:
        # TODO: Wrap the notifier call, and prefix with "[SMS] "
        pass


class SlackDecorator(NotifierDecorator):
    def send(self, message: str) -> str:
        # TODO: Wrap the notifier call, and prefix with "[Slack] "
        pass


# =====================================================================
# CLIENT / VERIFICATION CODE (Do not modify this part)
# =====================================================================

def verify_decorator():
    print("--- Testing Decorator (Multi-Layered Notifier) ---")
    
    # 1. Base notifier only
    try:
        notifier = BaseNotifier()
        res = notifier.send("System Alert")
        print(f"Base Notifier Result: {res}")
        assert res == "System Alert", f"❌ Failed: BaseNotifier altered the message."
        print("✅ Base Notifier: Success!")
    except Exception as e:
        print(f"❌ Base Notifier failed: {e}")

    # 2. Base + Email
    try:
        notifier = EmailDecorator(BaseNotifier())
        res = notifier.send("System Alert")
        print(f"Email Notifier Result: {res}")
        assert res == "[Email] System Alert", f"❌ Failed: EmailDecorator output incorrect."
        print("✅ Email Notifier: Success!")
    except Exception as e:
        print(f"❌ Email Notifier failed: {e}")

    # 3. Base + Email + SMS
    try:
        notifier = SMSDecorator(EmailDecorator(BaseNotifier()))
        res = notifier.send("System Alert")
        print(f"SMS + Email Notifier Result: {res}")
        assert res == "[SMS] [Email] System Alert", f"❌ Failed: SMS + Email output incorrect."
        print("✅ SMS + Email Notifier: Success!")
    except Exception as e:
        print(f"❌ SMS + Email Notifier failed: {e}")

    # 4. Base + Slack + SMS + Email
    try:
        notifier = EmailDecorator(SMSDecorator(SlackDecorator(BaseNotifier())))
        res = notifier.send("Critical Error")
        print(f"All Decorators Result: {res}")
        assert res == "[Email] [SMS] [Slack] Critical Error", f"❌ Failed: Full chain output incorrect."
        print("✅ Full Chain Notifier: Success!")
    except Exception as e:
        print(f"❌ Full Chain Notifier failed: {e}")


if __name__ == "__main__":
    verify_decorator()
