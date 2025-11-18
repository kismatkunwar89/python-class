import pymysql

try:
    print("Attempting to connect to MySQL database...")
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='chargerstore'
    )
    print("✓ Successfully connected to MySQL database!")

    cur = conn.cursor()

    # Test if customers table exists
    cur.execute("SHOW TABLES LIKE 'customers'")
    result = cur.fetchone()

    if result:
        print("✓ 'customers' table exists")

        # Count customers
        cur.execute("SELECT COUNT(*) FROM customers")
        count = cur.fetchone()[0]
        print(f"✓ Found {count} customers in the database")

        # Get sample customer
        cur.execute("SELECT customerNumber, customerName FROM customers LIMIT 1")
        sample = cur.fetchone()
        if sample:
            print(f"✓ Sample customer: #{sample[0]} - {sample[1]}")
    else:
        print("✗ 'customers' table not found")

    cur.close()
    conn.close()
    print("\n✓ Database connection test PASSED!")

except pymysql.err.OperationalError as e:
    print(f"✗ Connection failed: {e}")
    print("\nPossible issues:")
    print("- MySQL server is not running")
    print("- Wrong host/port (check if MySQL is on localhost:3306)")
    print("- Wrong username/password")
    print("- Database 'chargerstore' doesn't exist")
except Exception as e:
    print(f"✗ Error: {e}")
