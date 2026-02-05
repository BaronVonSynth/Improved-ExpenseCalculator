from tkinter import *
from tkinter import messagebox
from auth import *

###--COLORS--###
co1 = '#453934'  
co2 = "#55433B" 
co3 = "#301515"
co4 = "#FFFFFF"
co5 = '#644ced'
co6 = '#ed2f2f'
co8 = '#2fed68'

class LoginWindow:
    def __init__(self):
        self.logged_user = None
        self.window = Tk()
        self.window.title('Login - Expense Calculator')
        self.window.geometry('400x300')
        self.window.configure(background=co3)
        self.window.resizable(width=FALSE, height=FALSE)
        
        # Center window
        self.center_window()
        
        self.create_interface()
        
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_interface(self):
        # Title
        Label(self.window, text='Expense Calculator', font=('Verdana 18 bold'), 
              bg=co3, fg=co4).place(x=50, y=20)
        
        Label(self.window, text='Login to continue', font=('Verdana 10'), 
              bg=co3, fg=co4).place(x=100, y=60)
        
        # Form frame
        frame = Frame(self.window, bg=co1)
        frame.place(x=50, y=100, width=300, height=150)
        
        # Username
        Label(frame, text='Username:', font=('Ivy 10'), bg=co1, fg=co4).place(x=20, y=20)
        self.entry_username = Entry(frame, width=25, font=('Ivy 10'), relief='solid')
        self.entry_username.place(x=90, y=21)
        
        # Password
        Label(frame, text='Password:', font=('Ivy 10'), bg=co1, fg=co4).place(x=20, y=60)
        self.entry_password = Entry(frame, width=25, font=('Ivy 10'), relief='solid', show='*')
        self.entry_password.place(x=90, y=61)
        
        # Buttons
        Button(frame, text='Login', width=12, height=1, bg=co8, fg=co4, 
               font=('Ivy 9 bold'), relief='raised', command=self.perform_login).place(x=90, y=100)
        
        Button(frame, text='Register', width=12, height=1, bg=co5, fg=co4,
               font=('Ivy 9 bold'), relief='raised', command=self.open_registration).place(x=190, y=100)
        
        # Bind Enter to login
        self.entry_password.bind('<Return>', lambda e: self.perform_login())
    
    def perform_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showerror('Error', 'Fill in all fields!')
            return
        
        success, message = verify_login(username, password)
        
        if success:
            self.logged_user = username
            messagebox.showinfo('Success', f'Welcome, {username}!')
            self.window.destroy()
        else:
            messagebox.showerror('Error', message)
            self.entry_password.delete(0, END)
    
    def open_registration(self):
        registration_window = Toplevel(self.window)
        registration_window.title('User Registration')
        registration_window.geometry('400x350')
        registration_window.configure(background=co3)
        registration_window.resizable(width=FALSE, height=FALSE)
        
        # Center
        registration_window.update_idletasks()
        width = registration_window.winfo_width()
        height = registration_window.winfo_height()
        x = (registration_window.winfo_screenwidth() // 2) - (width // 2)
        y = (registration_window.winfo_screenheight() // 2) - (height // 2)
        registration_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Title
        Label(registration_window, text='New User Registration', font=('Verdana 14 bold'), 
              bg=co3, fg=co4).place(x=70, y=20)
        
        # Form frame
        frame = Frame(registration_window, bg=co1)
        frame.place(x=50, y=70, width=300, height=220)
        
        # Username
        Label(frame, text='Username:', font=('Ivy 10'), bg=co1, fg=co4).place(x=20, y=20)
        entry_new_username = Entry(frame, width=25, font=('Ivy 10'), relief='solid')
        entry_new_username.place(x=20, y=45)
        
        # Password
        Label(frame, text='Password:', font=('Ivy 10'), bg=co1, fg=co4).place(x=20, y=80)
        entry_new_password = Entry(frame, width=25, font=('Ivy 10'), relief='solid', show='*')
        entry_new_password.place(x=20, y=105)
        
        # Confirm password
        Label(frame, text='Confirm Password:', font=('Ivy 10'), bg=co1, fg=co4).place(x=20, y=140)
        entry_confirm_password = Entry(frame, width=25, font=('Ivy 10'), relief='solid', show='*')
        entry_confirm_password.place(x=20, y=165)
        
        def perform_registration():
            username = entry_new_username.get().strip()
            password = entry_new_password.get()
            confirm = entry_confirm_password.get()
            
            if not username or not password or not confirm:
                messagebox.showerror('Error', 'Fill in all fields!')
                return
            
            if len(username) < 3:
                messagebox.showerror('Error', 'Username must have at least 3 characters!')
                return
            
            if len(password) < 4:
                messagebox.showerror('Error', 'Password must have at least 4 characters!')
                return
            
            if password != confirm:
                messagebox.showerror('Error', 'Passwords do not match!')
                return
            
            success, message = register_user(username, password)
            
            if success:
                messagebox.showinfo('Success', message)
                registration_window.destroy()
            else:
                messagebox.showerror('Error', message)
        
        # Register button
        Button(frame, text='Register', width=15, height=1, bg=co8, fg=co4,
               font=('Ivy 9 bold'), relief='raised', command=perform_registration).place(x=80, y=195)
        
        # Bind Enter
        entry_confirm_password.bind('<Return>', lambda e: perform_registration())
    
    def run(self):
        self.window.mainloop()
        return self.logged_user

# Function to run login
def run_login():
    login = LoginWindow()
    user = login.run()
    return user
