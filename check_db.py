import sqlite3

conn = sqlite3.connect('output/db.libsql')

print("Tables:")
for table in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
    print(f"  {table[0]}")

print("\nZomato Accounts:")
for row in conn.execute("SELECT * FROM zomato_accounts").fetchall():
    print(f"  {row}")

print("\nZomato Orders (first 3):")
for row in conn.execute("SELECT order_id, total_cost, dish_string, delivery_label FROM zomato_orders LIMIT 3").fetchall():
    print(f"  {row}")

print(f"\nTotal Orders: {conn.execute('SELECT COUNT(*) FROM zomato_orders').fetchone()[0]}")

conn.close()
