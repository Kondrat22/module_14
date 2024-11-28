import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMERY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)               
''')

# for i in range(1, 11):
#    cursor.execute("INSERT INTO Users (id, username, email, age, balance) VALUES (?, ?, ?, ?, ?)",
#                   (f"{i}", f"User{i}", f"example{i}@gmail.com", f"{i}0", "1000"))

# for i in range(1, 11, 2):
#    cursor.execute(
#        "UPDATE Users SET balance = 500 WHERE username = ?", (f"User{i}",))

# for i in range(1, 11, 3):
#    cursor.execute("DELETE FROM Users WHERE username = ?", (f"User{i}",))

# cursor.execute(
#    "SELECT username, email, age, balance FROM Users WHERE age != 60")
# users = cursor.fetchall()
# for user in users:
#    print("Имя:", user[0], "|", "Почта:", user[1], "|",
#          "Возраст:", user[2], "|", "Баланс:", user[3])

cursor.execute("DELETE FROM Users WHERE id = ?", ("6",))

cursor.execute("SELECT COUNT (*) FROM Users")
total1 = cursor.fetchone()[0]

cursor.execute("SELECT SUM(balance) FROM Users")
total2 = cursor.fetchone()[0]

print(total2/total1)

connection.commit()
connection.close()
