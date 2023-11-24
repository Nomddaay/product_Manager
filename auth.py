import csv
import tkinter as tk
from tkinter import messagebox
from user import User
from dashboard import Dashboard

class AuthScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login / Registration")
        self.geometry("300x200")

        self.label_username = tk.Label(self, text="Username:")
        self.label_password = tk.Label(self, text="Password:")

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        self.button_action = tk.Button(self, text="Login", command=self.login_or_register)
        self.button_switch = tk.Button(self, text="Switch to Register", command=self.switch_mode)

        # Set the initial mode to login
        self.is_register_mode = False
        self.update_ui()

    def login_or_register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.is_register_mode:
            self.register(username, password)
        else:
            self.login(username, password)

    def login(self, username, password):
        if self.authenticate(username, password):
            self.destroy()
            app = Dashboard()
            app.geometry("1000x650")
            app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self, username, password):
        if not username or not password:
            messagebox.showerror("Registration Failed", "Please enter both username and password.")
            return

        if self.username_exists(username):
            messagebox.showerror("Registration Failed", "Username already exists. Choose a different username.")
            return

        new_user = User(username, password)
        self.save_user_to_csv(new_user)

        messagebox.showinfo("Registration Successful", "Registration successful. You can now login.")
        self.switch_mode()

    def authenticate(self, username, password):
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username and row[1] == password:
                    return True
        return False

    def username_exists(self, username):
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username:
                    return True
        return False

    def save_user_to_csv(self, user):
        with open("users.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([user.username, user.password])
            file.write("\n")

    def switch_mode(self):
        self.is_register_mode = not self.is_register_mode
        self.update_ui()

    def update_ui(self):
        if self.is_register_mode:
            self.title("Registration")
            self.button_action.config(text="Register")
            self.button_switch.config(text="Login")
        else:
            self.title("Login")
            self.button_action.config(text="Login")
            self.button_switch.config(text="Register")

        # Clear entry fields
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

        self.label_username.grid(row=0, column=0, pady=(20, 0), padx=10, sticky="w")
        self.label_password.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.entry_username.grid(row=0, column=1, pady=(20, 0), padx=10, sticky="e")
        self.entry_password.grid(row=1, column=1, pady=10, padx=10, sticky="e")
        self.button_action.grid(row=2, column=0, pady=10, sticky="e")
        self.button_switch.grid(row=2, column=1, pady=10, sticky="e")

