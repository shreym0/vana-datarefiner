#!/usr/bin/env python3

import sqlite3
import json

def check_database():
    db_path = "output/db.libsql"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("=== DATABASE TABLES ===")
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"Row count: {count}")
            
            # Show some sample data if exists
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
                rows = cursor.fetchall()
                print("Sample data:")
                for row in rows:
                    print(f"  {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error reading database: {e}")

if __name__ == "__main__":
    check_database()
