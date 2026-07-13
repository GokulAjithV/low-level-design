import threading
import time
from abc import ABC, abstractmethod

# =====================================================================
# CHALLENGE: Thread-Safe Configuration Manager (Solution)
# =====================================================================

class ConfigurationManager:
    _instance = None
    _lock = threading.Lock()
    _init_count = 0

    def __new__(cls, *args, **kwargs):
        # Double-Checked Locking
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Double-checked initialization check to prevent repeated runs
        if not hasattr(self, '_initialized'):
            with self._lock:
                if not hasattr(self, '_initialized'):
                    self.config = {}
                    self._initialized = True
                    self.__class__._init_count += 1

    def load_config(self, config_dict: dict):
        with self._lock:
            # Simple simulation: only load config if it is currently empty
            if not self.config:
                self.config.update(config_dict)

    def get(self, key: str):
        with self._lock:
            return self.config.get(key, None)


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
