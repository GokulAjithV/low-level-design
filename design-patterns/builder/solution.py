# =====================================================================
# CHALLENGE: Fluent SQL Query Builder (Solution)
# =====================================================================

class SQLQueryBuilder:
    def __init__(self):
        self._columns = None
        self._table_name = None
        self._wheres = []
        self._limit = None

    def select(self, columns):
        if isinstance(columns, list):
            self._columns = ", ".join(columns)
        else:
            self._columns = columns
        return self

    def from_table(self, table_name: str):
        self._table_name = table_name
        return self

    def where(self, condition: str):
        self._wheres.append(condition)
        return self

    def limit(self, count: int):
        self._limit = count
        return self

    def build(self) -> str:
        if not self._columns:
            raise ValueError("SELECT columns must be defined")
        if not self._table_name:
            raise ValueError("FROM table name must be defined")

        query = f"SELECT {self._columns} FROM {self._table_name}"
        
        if self._wheres:
            query += f" WHERE {' AND '.join(self._wheres)}"
        
        if self._limit is not None:
            query += f" LIMIT {self._limit}"
            
        query += ";"
        return query


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
