import sqlite3

# 1. Connect to the database (this creates a file called 'test.db')
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# 2. Create a table called 'users'
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
""")

# 3. Add some data
users_data = [
    ("Alice", 25),
    ("Bob", 17),
    ("Charlie", 30),
    ("Diana", 22)
]
cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users_data)
conn.commit() # Save the changes

# ==========================================
# YOUR TURN! WRITE YOUR SQL QUERIES BELOW:
# ==========================================

# Task 1: Write a query to get ALL users
cursor.execute("SELECT * FROM users")
print("All users:", cursor.fetchall())

# Task 2: Write a query to get ONLY users who are 18 or older
cursor.execute("SELECT * FROM users WHERE age >= 18")
print("Adults:", cursor.fetchall())

# Task 3: Write a query to get users ordered by age (oldest to youngest)
cursor.execute("SELECT * FROM users ORDER BY age DESC")
print("Sorted by age:", cursor.fetchall())

# Task 4: Add a new user named "Eve" who is 28 years old
# (Hint: use cursor.execute with INSERT INTO)
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Eve", 28))
conn.commit()
print("Eve added!")

# 4. Close the connection
conn.close()