# =====================================================================
# CHALLENGE: Fluent SQL Query Builder
# =====================================================================

class SQLQueryBuilder:
    def __init__(self):
        # TODO: Initialize attributes to store select columns, table, where conditions, and limit.
        pass

    def select(self, columns):
        # TODO: Store the columns. Handle both string (e.g. "id, name") and list of strings.
        # Hint: Return self to enable method chaining.
        pass

    def from_table(self, table_name: str):
        # TODO: Store the table name.
        # Hint: Return self to enable method chaining.
        pass

    def where(self, condition: str):
        # TODO: Append the condition to a list of where conditions.
        # Hint: Return self to enable method chaining.
        pass

    def limit(self, count: int):
        # TODO: Store the limit count.
        # Hint: Return self to enable method chaining.
        pass

    def build(self) -> str:
        # TODO: Construct and return the SQL query string.
        # Format guidelines:
        # - Must start with "SELECT <columns> FROM <table_name>"
        # - If there are WHERE conditions, join them using " AND " (e.g. " WHERE cond1 AND cond2")
        # - If there is a LIMIT, append " LIMIT <count>"
        # - Append a semicolon ";" at the end of the query.
        # - Raise a ValueError if select() or from_table() was not set.
        pass


# =====================================================================
# CLIENT / VERIFICATION CODE (Do not modify this part)
# =====================================================================

def verify_builder():
    print("--- Testing Builder (SQL Query Builder) ---")
    
    # Test case 1: Standard query with all fields
    try:
        builder = SQLQueryBuilder()
        query = (builder
                 .select(["id", "name", "email"])
                 .from_table("users")
                 .where("age > 18")
                 .where("status = 'active'")
                 .limit(5)
                 .build())
        
        expected = "SELECT id, name, email FROM users WHERE age > 18 AND status = 'active' LIMIT 5;"
        print(f"Generated Query 1: {query}")
        assert query == expected, f"❌ Failed: Expected '{expected}', got '{query}'"
        print("✅ Query 1 building: Success!")
    except Exception as e:
        print(f"❌ Query 1 failed with error: {e}")

    # Test case 2: String format columns & no limit or where
    try:
        builder = SQLQueryBuilder()
        query = (builder
                 .select("count(*)")
                 .from_table("orders")
                 .build())
        
        expected = "SELECT count(*) FROM orders;"
        print(f"Generated Query 2: {query}")
        assert query == expected, f"❌ Failed: Expected '{expected}', got '{query}'"
        print("✅ Query 2 building: Success!")
    except Exception as e:
        print(f"❌ Query 2 failed with error: {e}")

    # Test case 3: Validation checks (ValueError)
    try:
        builder = SQLQueryBuilder()
        builder.from_table("products").build()
        print("❌ Failed: Should have raised ValueError due to missing SELECT columns.")
    except ValueError:
        print("✅ Validation (Missing SELECT) raises ValueError: Success!")
    except Exception as e:
        print(f"❌ Validation failed with unexpected error: {e}")

    try:
        builder = SQLQueryBuilder()
        builder.select("id").build()
        print("❌ Failed: Should have raised ValueError due to missing FROM table.")
    except ValueError:
        print("✅ Validation (Missing FROM) raises ValueError: Success!")
    except Exception as e:
        print(f"❌ Validation failed with unexpected error: {e}")


if __name__ == "__main__":
    verify_builder()
