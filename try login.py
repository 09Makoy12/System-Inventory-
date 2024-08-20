import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import Administrator
import Spectator

class PlaceholderEntry(tk.Entry):
    """Entry widget with placeholder text and optional password masking."""
    def __init__(self, master=None, placeholder="", show="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.show = show  # For password masking
        self.config(show='', bg='white')  # No masking initially and background color
        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)
        self.bind("<KeyRelease>", self.handle_key_release)
        self.add_placeholder()

    def add_placeholder(self, *args):
        """Add placeholder if the entry is empty."""
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg='grey')
            self.config(show='')  # Show placeholder text without masking
        else:
            self.config(fg='black')

    def remove_placeholder(self, *args):
        """Remove placeholder when focus is gained."""
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg='black')
        self.config(show=self.show)  # Apply masking if configured

    def handle_key_release(self, *args):
        """Handle key release event to manage placeholder and show masking."""
        if self.get() == self.placeholder:
            self.config(fg='grey')
        else:
            self.config(fg='black')
            self.config(show=self.show)  # Apply masking if configured

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management System")
        self.geometry("725x450")  # Initial size
        self.configure(bg="#fff")
        self.resizable(True, True)  # Allow resizing

        try:
            self.iconphoto(True, ImageTk.PhotoImage(Image.open('logo1.png')))
        except Exception as e:
            print(f"Error setting icon: {e}")

        # Calculate the position to center the window
        window_width = 725
        window_height = 425
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # Main Frame
        main_frame = tk.Frame(self, bg="#fff")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame for the Image
        self.image_frame = tk.Frame(main_frame, bg='white')
        self.image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20, expand=True)

        # Frame for the Login Form (Blend with background)
        self.form_frame = tk.Frame(main_frame, bg="#fff", bd=0, relief=tk.FLAT)  # Same background color, no border
        self.form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=20, pady=20, expand=True)

        # Load and set the image
        try:
            self.image = Image.open("logo1.png")  # Change "logo1.png" to your image file
            self.image = self.image.resize((290, 290), Image.Resampling.LANCZOS)
            self.image_photo = ImageTk.PhotoImage(self.image)
            self.image_label = tk.Label(self.image_frame, image=self.image_photo, bg='white')
            self.image_label.pack(padx=30, pady=30)
        except Exception as e:
            print(f"Error loading image: {e}")

        # Heading
        tk.Label(self.form_frame, text='Sign In', fg='#57a1f8', bg='white', font=('Microsoft Tai Le', 23, 'bold')).pack(pady=(20, 10))

        # Username Entry with Placeholder
        self.username_entry = PlaceholderEntry(self.form_frame, placeholder="Username", width=30, fg='black', border=0, bg="white", font=('Microsoft Tai Le', 11))
        self.username_entry.pack(pady=(35, 1), padx=20, fill=tk.X)
        tk.Frame(self.form_frame, height=2, bg='black').pack(pady=(0, 10), padx=20, fill=tk.X)

        # Password Entry with Placeholder and Masking
        self.password_entry = PlaceholderEntry(self.form_frame, placeholder='Password', width=30, fg='black', border=0, bg='white', font=('Microsoft Tai Le', 11), show='*')
        self.password_entry.pack(pady=(35, 1), padx=20, fill=tk.X)
        tk.Frame(self.form_frame, height=2, bg='black').pack(pady=(0, 20), padx=20, fill=tk.X)

        # Login Button
        tk.Button(self.form_frame, width=20, pady=10, text='Sign In', bg='#57a1f8', fg='white', border=0, font=('Microsoft Tai Le', 12, 'bold'), command=self.check_login).pack(pady=(20, 10))

        # Additional Button
        tk.Button(self.form_frame, width=17, text='Open as Spectator', border=0, bg='white', cursor='hand2', fg='#57a1f8', font=('Microsoft Tai Le', 10), command=self.spectator_login).pack(pady=(10, 20))

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "password":
            self.destroy()  # Close the login window
            Administrator.run_app()  # Run the main application
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def spectator_login(self):
        
        messagebox.showinfo("As Spectator", "Welcome Spectator")

        Spectator.run_app()  # Run the main application
            
if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
