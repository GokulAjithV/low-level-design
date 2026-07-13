from abc import ABC, abstractmethod

# =====================================================================
# CHALLENGE: Dynamic Sorting Tool
# =====================================================================

# 1. Define the Abstract Strategy
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass


# 2. Implement Concrete Strategies
class BubbleSort(SortStrategy):
    def sort(self, data: list) -> list:
        # TODO: Implement Bubble Sort algorithm
        # Hint: Work on a copy of the list (e.g. data.copy() or list(data)) so as not to mutate the original.
        pass


class QuickSort(SortStrategy):
    def sort(self, data: list) -> list:
        # TODO: Implement Quick Sort algorithm (or mock it using Python's sorted() but named/structured as QuickSort)
        pass


class MergeSort(SortStrategy):
    def sort(self, data: list) -> list:
        # TODO: Implement Merge Sort algorithm (or mock it using Python's sorted() but named/structured as MergeSort)
        pass


# 3. Define the Context Class
class Sorter:
    def __init__(self, strategy: SortStrategy):
        # TODO: Initialize with a default sorting strategy
        pass

    def set_strategy(self, strategy: SortStrategy):
        # TODO: Allow changing strategy dynamically
        pass

    def execute_sort(self, data: list) -> list:
        # TODO: Execute the sort using the selected strategy
        pass


# =====================================================================
# CLIENT / VERIFICATION CODE (Do not modify this part)
# =====================================================================

def verify_strategy():
    print("--- Testing Strategy (Dynamic Sorting Tool) ---")
    data = [5, 2, 9, 1, 5, 6]
    
    # 1. Test Bubble Sort
    try:
        sorter = Sorter(BubbleSort())
        res = sorter.execute_sort(data)
        print(f"Bubble Sort Result: {res}")
        assert res == [1, 2, 5, 5, 6, 9], "❌ Failed: BubbleSort did not sort correctly."
        print("✅ Bubble Sort: Success!")
    except Exception as e:
        print(f"❌ Bubble Sort failed: {e}")

    # 2. Test Quick Sort
    try:
        sorter = Sorter(QuickSort())
        res = sorter.execute_sort(data)
        print(f"Quick Sort Result: {res}")
        assert res == [1, 2, 5, 5, 6, 9], "❌ Failed: QuickSort did not sort correctly."
        print("✅ Quick Sort: Success!")
    except Exception as e:
        print(f"❌ Quick Sort failed: {e}")

    # 3. Test Merge Sort
    try:
        sorter = Sorter(MergeSort())
        res = sorter.execute_sort(data)
        print(f"Merge Sort Result: {res}")
        assert res == [1, 2, 5, 5, 6, 9], "❌ Failed: MergeSort did not sort correctly."
        print("✅ Merge Sort: Success!")
    except Exception as e:
        print(f"❌ Merge Sort failed: {e}")

    # 4. Test Dynamic Swap
    try:
        sorter = Sorter(BubbleSort())
        # Swap strategy at runtime
        sorter.set_strategy(MergeSort())
        res = sorter.execute_sort(data)
        assert res == [1, 2, 5, 5, 6, 9], "❌ Failed: Strategy swap did not work."
        print("✅ Dynamic Strategy Swapping: Success!")
    except Exception as e:
        print(f"❌ Dynamic Strategy Swapping failed: {e}")


if __name__ == "__main__":
    verify_strategy()
