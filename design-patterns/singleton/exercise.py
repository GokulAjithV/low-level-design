import threading
import time
from abc import ABC, abstractmethod

# =====================================================================
# CHALLENGE: Thread-Safe Configuration Manager
# =====================================================================

class ConfigurationManager:
    _instance = None
    _lock = threading.Lock()
    
    # Track the number of times initialization/loading occurs
    _init_count = 0

    def __new__(cls, *args, **kwargs):
        # TODO: Implement double-checked locking singleton instantiation
        pass

    def __init__(self):
        # We only want setup logic to run ONCE across the entire lifecycle.
        # Python's default behavior executes __init__ every time class() is called.
        # TODO: Guard the initialization logic so that _init_count is only incremented on the first initialization,
        # and self.config is only set up once.
        pass

    def load_config(self, config_dict: dict):
        # TODO: Store the dictionary values in self.config if not already loaded.
        # Hint: This is only done once, or you can merge it. For this exercise, 
        # let's assume config is loaded once.
        pass

    def get(self, key: str):
        # TODO: Return the configuration value for key. Return None if key doesn't exist.
        pass


# =====================================================================
# CLIENT / VERIFICATION CODE (Do not modify this part)
# =====================================================================

def thread_task(name: int, barrier: threading.Barrier, results: list):
    # Wait for all threads to be ready to simulate high concurrency
    barrier.wait()
    
    # Try to get the instance
    config_mgr = ConfigurationManager()
    
    # Attempt to load config (only the first thread or initial setup should succeed/set the state)
    config_mgr.load_config({"app_name": "AntigravityApp", "version": "1.0"})
    
    # Retrieve a value
    app_name = config_mgr.get("app_name")
    
    # Append the retrieved value and instance ID to verify they are all the same instance
    results.append((id(config_mgr), app_name))


def verify_singleton():
    print("--- Testing Singleton (Configuration Manager) ---")
    threads = []
    num_threads = 10
    barrier = threading.Barrier(num_threads)
    results = []

    for i in range(num_threads):
        t = threading.Thread(target=thread_task, args=(i, barrier, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Verify all threads retrieved the same instance ID and configuration value
    instance_ids = {res[0] for res in results}
    config_vals = {res[1] for res in results}
    
    # Verify singleton instances
    print(f"Unique instances created: {len(instance_ids)}")
    print(f"ConfigurationManager __init__ run count: {ConfigurationManager._init_count}")
    
    try:
        assert len(instance_ids) == 1, "❌ Failed: Multiple instances of ConfigurationManager were created!"
        assert ConfigurationManager._init_count == 1, "❌ Failed: __init__ was run more than once!"
        assert list(config_vals)[0] == "AntigravityApp", "❌ Failed: Configuration parameters were not loaded correctly!"
        
        # Test getting a non-existent key
        mgr = ConfigurationManager()
        assert mgr.get("non_existent") is None, "❌ Failed: Should return None for missing keys"
        
        print("✅ Singleton Challenge: Success!")
    except AssertionError as e:
        print(e)
    except Exception as e:
        print(f"❌ Failed with unexpected error: {e}")

if __name__ == "__main__":
    verify_singleton()
