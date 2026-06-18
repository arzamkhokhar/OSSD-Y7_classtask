import sqlite3

con = sqlite3.connect("project.db")
cursor = con.cursor()

V1 = input("Enter username: ")
V2 = input("Enter email: ")
V3 = input("Enter password: ")

t = (V1, V2, V3)

cursor.execute("""
CREATE TABLE IF NOT EXISTS LOGIN_INFO(
    USERNAME TEXT PRIMARY KEY,
    EMAIL TEXT NOT NULL,
    PASSWORD TEXT NOT NULL
)
""")

cursor.execute(
    "INSERT INTO LOGIN_INFO (USERNAME, EMAIL, PASSWORD) VALUES (?, ?, ?)",
    t
)

print("Data inserted successfully")

con.commit()
con.close()