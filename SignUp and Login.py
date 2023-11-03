import tkinter as tk
import sqlite3
import subprocess
from Project import PhotoshopApp

# Create a SQLite database and table for storing user information
db_conn = sqlite3.connect('user_database.db')
db_cursor = db_conn.cursor()
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
''')
db_conn.commit()

class Login:
    def __init__(self, root):
        self.root = root
        self.signup_window = None
        self.root.title("Login Page")
        self.root.geometry("300x200")

        self.username_label = tk.Label(root, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

        self.signup_link = tk.Label(root, text="Don't have an account? Sign up here", cursor="hand2")
        self.signup_link.pack()
        self.signup_link.bind("<Button-1>", self.go_to_signup)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        db_cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        result = db_cursor.fetchone()

        if result:
            print("Login successful")
            subprocess.Popen(["python", "project.py"])
        else:
            print("Login failed")

    def go_to_signup(self, event):
        if self.signup_window is None:
            self.signup_window = tk.Tk()
            signup_page = Signup(self.signup_window, self)
            signup_page.root.protocol("WM_DELETE_WINDOW", self.close_signup)
        self.root.withdraw()
        self.signup_window.deiconify()

    def close_signup(self):
        self.signup_window.withdraw()
        self.root.deiconify()

class Signup:
    def __init__(self, root, login_page):
        self.root = root
        self.login_page = login_page
        self.root.title("Signup Page")
        self.root.geometry("300x200")

        self.username_label = tk.Label(root, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.signup_button = tk.Button(root, text="Signup", command=self.signup)
        self.signup_button.pack()

        self.login_link = tk.Label(root, text="Already have an account? Login here", cursor="hand2")
        self.login_link.pack()
        self.login_link.bind("<Button-1>", self.go_to_login)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        db_cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db_conn.commit()

        print("Signup successful")
        self.root.withdraw()
        self.login_page.root.deiconify()

    def go_to_login(self, event):
        self.root.withdraw()
        self.login_page.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    login = Login(root)
    root.mainloop()

db_conn.close()
