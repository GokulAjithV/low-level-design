from abc import ABC, abstractmethod

# =====================================================================
# CHALLENGE: Dynamic Sorting Tool (Solution)
# =====================================================================

# 1. Define the Abstract Strategy
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass


# 2. Implement Concrete Strategies
class BubbleSort(SortStrategy):
    def sort(self, data: list) -> list:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class QuickSort(SortStrategy):
    def sort(self, data: list) -> list:
        def _quicksort(arr):
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return _quicksort(left) + middle + _quicksort(right)
        return _quicksort(data)


class MergeSort(SortStrategy):
    def sort(self, data: list) -> list:
        def _mergesort(arr):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = _mergesort(arr[:mid])
            right = _mergesort(arr[mid:])
            return _merge(left, right)
            
        def _merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result
            
        return _mergesort(data)


# 3. Define the Context Class
class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def execute_sort(self, data: list) -> list:
        return self._strategy.sort(data)


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
