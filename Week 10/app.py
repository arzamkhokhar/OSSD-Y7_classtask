import tkinter as tk
import tkinter.messagebox as messagebox

# File to store users
USER_FILE = "users.txt"

def read_file():
    users = {}

    try:
        file = open("users.txt", "r")
        
        for line in file:
             parts = line.strip().split(":")
             if len(parts) == 3:
                 username, email, password = parts
                 users[username] = {"email": email, "password": password}
             else:
                 # Handle old format (username:password)
                 username, password = parts
                 users[username] = {"email": "", "password": password}
            
        file.close()
    except FileNotFoundError:
        pass # If the file doesn't exist, just do nothing

    return users

def write_file(users):
    with open(USER_FILE, "w") as f:
        for username, user_data in users.items():
            email = user_data.get("email", "")
            password = user_data.get("password", "")
            f.write(f"{username}:{email}:{password}\n")

def show_options():
    root.withdraw()  # Hide login window
    
    options_window = tk.Toplevel(root)
    options_window.title("Options")
    options_window.geometry("300x270")
    options_window.resizable(False, False)
    
    tk.Label(options_window, text="Choose an option:", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Button(options_window, text="Option 1", width=20).pack(pady=5)
    tk.Button(options_window, text="Option 2", width=20).pack(pady=5)
    tk.Button(options_window, text="Option 3", width=20).pack(pady=5)
    
    def on_close():
        options_window.destroy()
        root.deiconify()  # Show login window again
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    
    tk.Button(options_window, text="Sign Out", width=20, fg="red", command=on_close).pack(pady=10)
    
    options_window.protocol("WM_DELETE_WINDOW", on_close)

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username in users and users[username]["password"] == password:
        messagebox.showinfo("Success", "Login successful!")
        show_options()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def signup():
    global email_entry, email_label, register_button, back_button, login_button, signup_button
    
    # Hide login and signup buttons
    login_button.pack_forget()
    signup_button.pack_forget()
    
    # Show email label and entry
    email_label.pack(pady=5)
    email_entry.pack(pady=5)
    
    # Show register and back buttons
    register_button.pack(pady=10)
    back_button.pack(pady=5)

def register():
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    
    if not username or not email or not password:
        messagebox.showerror("Error", "All fields cannot be empty")
        return
    
    if username in users:
        messagebox.showerror("Error", "Username already exists")
        return
    
    users[username] = {"email": email, "password": password}
    write_file(users)
    messagebox.showinfo("Success", "Signup successful!")
    back_to_login()

def back_to_login():
    global email_entry, email_label, register_button, back_button, login_button, signup_button
    
    # Hide email field and register/back buttons
    email_label.pack_forget()
    email_entry.pack_forget()
    register_button.pack_forget()
    back_button.pack_forget()
    
    # Show login and signup buttons
    login_button.pack(pady=10)
    signup_button.pack(pady=10)
    
    # Clear all fields
    username_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def main():
    global root, username_entry, password_entry, email_entry, email_label, register_button, back_button, login_button, signup_button, users
    users = read_file()
    
    root = tk.Tk()
    root.title("Login System")
    root.geometry("300x250")
    root.resizable(False, False)
    
    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)
    
    tk.Label(root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)
    
    # Email label and entry (initially hidden)
    email_label = tk.Label(root, text="Email:")
    email_entry = tk.Entry(root)
    
    login_button = tk.Button(root, text="Login", command=login)
    login_button.pack(pady=10)
    
    signup_button = tk.Button(root, text="Signup", command=signup)
    signup_button.pack(pady=10)
    
    # Register and Back buttons (initially hidden)
    register_button = tk.Button(root, text="Register", command=register, width=20)
    back_button = tk.Button(root, text="Back to Login", command=back_to_login, width=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()