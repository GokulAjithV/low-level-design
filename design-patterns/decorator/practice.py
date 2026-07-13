from abc import ABC, abstractmethod

# Step 1: The Abstract Component (The Contract)
class TournamentFeature(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> int:
        pass


# Step 2: The Concrete Component (The Core Object)
class CoreScorecard(TournamentFeature):
    def get_description(self) -> str:
        return "Standard Ball-by-Ball Scoring Engine"

    def get_cost(self) -> int:
        return 1000  # Base price in INR


# Step 3: The Abstract Decorator (Wraps a TournamentFeature)
class FeatureDecorator(TournamentFeature, ABC):
    def __init__(self, feature: TournamentFeature):
        self._wrapped_feature = feature  # Composition

    def get_description(self) -> str:
        return self._wrapped_feature.get_description()

    def get_cost(self) -> int:
        return self._wrapped_feature.get_cost()


# Step 4: Concrete Decorators (The Add-ons)
class LiveStreamingDecorator(FeatureDecorator):
    def get_description(self) -> str:
        # Adds its own description to the wrapped object's description
        return self._wrapped_feature.get_description() + " + HD Live Streaming API"

    def get_cost(self) -> int:
        # Adds its own cost to the wrapped object's cost
        return self._wrapped_feature.get_cost() + 500


class AIAnalyticsDecorator(FeatureDecorator):
    def get_description(self) -> str:
        return self._wrapped_feature.get_description() + " + AI Player Performance Analytics"

    def get_cost(self) -> int:
        return self._wrapped_feature.get_cost() + 800


if __name__ == "__main__":

    # 1. Customer wants just the basic package
    package = CoreScorecard()
    print(f"Package A: {package.get_description()} | Total Cost: ₹{package.get_cost()}")

    # 2. Customer wants to add Live Streaming at runtime
    package_with_stream = LiveStreamingDecorator(package)
    print(f"Package B: {package_with_stream.get_description()} | Total Cost: ₹{package_with_stream.get_cost()}")

    # 3. Customer wants EVERYTHING (Layering multiple decorators)
    premium_package = AIAnalyticsDecorator(package_with_stream)
    print(f"Package C: {premium_package.get_description()} | Total Cost: ₹{premium_package.get_cost()}")