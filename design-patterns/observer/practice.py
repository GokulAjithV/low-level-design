from abc import ABC, abstractmethod

# Step 1: Define the Abstract Observer (The Subscriber Contract)
class ScoreObserver(ABC):
    @abstractmethod
    def update(self, score, wickets):
        pass

# Step 2: Implement Concrete Observers (The Independent Subsystems)
class WebDashboard(ScoreObserver):
    def update(self, score: int, wickets: int):
        print(f"🖥️ [UI Dashboard] Refreshing display score to: {score}/{wickets}")

class SMSNotificationSystem(ScoreObserver):
    def update(self, score: int, wickets: int):
        print(f"📱 [SMS Alert] Sending text: Live score is now {score}/{wickets}")

# Step 2: Define the Subject (The Publisher Engine)
class ScorePublisher:
    def __init__(self):
        self._observers = []
        self._score = 0
        self._wickets = 0

    def attach(self, observer: ScoreObserver):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: ScoreObserver):
        self._observers.remove(observer)

    def notify_all(self):
        for observer in self._observers:
            observer.update(self._score, self._wickets)

    def update_score(self, runs, lost_wicket: bool = False):
        self._score += runs
        if lost_wicket:
            self._wickets += 1
        print(f"🏏 Match Update: {self._score}/{self._wickets}")
        # Automatically trigger the broadcast    
        self.notify_all()

# Core business engine
match_center = ScorePublisher()

# Independent frontend/backend components
ui_display = WebDashboard()
sms_alert = SMSNotificationSystem()

# Subscribe them to the match engine
match_center.attach(ui_display)
match_center.attach(sms_alert)

# Update score -> Automatically broadcasts to all attached services
match_center.update_score(6)

print("\n--- User unsubscribes from SMS alerts ---")
match_center.detach(sms_alert)

# Next ball update only targets active subscribers
match_center.update_score(1, lost_wicket=True)