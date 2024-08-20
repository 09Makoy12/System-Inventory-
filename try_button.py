import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

RIGHT_FRAME_WIDTH = 400  # Example width
RIGHT_FRAME_HEIGHT = 600 # Example height

# Global list to store individuals' data
individuals = []

# List of office options for the dropdown
OFFICE_OPTIONS = ["Mayor's Office", 'Vice Mayor Office', 'Accounting Office', 'Administrative Office', "Assessor's Office", 'BPLO', 'Budget Office', 
                  'Community Affairs', 'MEO', 'MPDC', 'MTO', 'COMELEC', 'SB Sec', 'SB Leg', 'DILG', 'HRMO', 'ICTS', 'MDRRMO']
 
class AddItemDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Transactions")
        
        # Create and place widgets for input fields
        labels = ["Product Name", "Product Type", "Product Model", "Serial Number", "Office", "Received by", "Borrowed by", "Date", "Quantity"]
        self.entries = {}
        
        for idx, label in enumerate(labels):
            tk.Label(self, text=f"{label}:", font=('Helvetica', 10)).grid(row=idx, column=0, padx=5, pady=5, sticky='w')
            
            if label == "Date":
                # Use DateEntry widget for the Date field with a simplified style
                entry = DateEntry(self, width=18, font=('Helvetica', 10), background='lightblue', foreground='black', borderwidth=2, date_pattern='y-mm-dd')
            elif label == "Office":
                # Use Combobox widget for the Office field
                entry = ttk.Combobox(self, values=OFFICE_OPTIONS, width=18, font=('Helvetica', 10))
            else:
                entry = tk.Entry(self, width=20, font=('Helvetica', 10))
            
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
            self.entries[label] = entry

        self.btn_add = tk.Button(self, text="Add", width=12, font=('Helvetica', 10), command=self.add_or_edit_individual)
        self.btn_add.grid(row=len(labels), column=1, padx=10, pady=10, sticky='e')

        self.current_index = None  # To store the index of the item being edited

    def set_edit_mode(self, index):
        self.current_index = index
        data = individuals[index]
        for label, entry in zip(["Product Name", "Product Type", "Product Model", "Serial Number", "Office", "Received by", "Borrowed by", "Date", "Quantity"], self.entries.values()):
            if label == "Date":
                # Set the date for the DateEntry widget
                entry.set_date(data[label])
            elif label == "Office":
                # Set the selected value for the Combobox
                entry.set(data[label])
            else:
                entry.delete(0, tk.END)
                entry.insert(0, data[label])

    def add_or_edit_individual(self):
        try:
            # Check if all fields are filled
            data = {label: entry.get() for label, entry in self.entries.items()}
            if any(value.strip() == "" for value in data.values()):
                messagebox.showerror("Error", "All fields must be filled out.")
                return
            
            if self.current_index is None:
                # Add mode
                individuals.append(data)
                messagebox.showinfo("Success", "Individual added successfully.")
            else:
                # Edit mode
                individuals[self.current_index] = data
                messagebox.showinfo("Success", "Individual updated successfully.")
                self.current_index = None  # Reset edit mode

            self.destroy()  # Close the dialog after adding or editing
            populate_treeview()  # Update treeview with new data
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data.")

def edit_individual():
    try:
        selected_item = treeview.selection()[0]
        index = treeview.index(selected_item)
        dialog = AddItemDialog(root)
        dialog.set_edit_mode(index)
    except IndexError:
        messagebox.showerror("Error", "Please select an individual to edit.")

def delete_individual():
    try:
        selected_item = treeview.selection()[0]
        index = treeview.index(selected_item)
        individuals.pop(index)
        messagebox.showinfo("Success", "Individual deleted successfully.")
        populate_treeview()  # Update treeview after deletion
    except IndexError:
        messagebox.showerror("Error", "Please select an individual to delete.")

def populate_treeview(filtered_individuals=None):
    treeview.delete(*treeview.get_children())
    data = filtered_individuals if filtered_individuals is not None else individuals
    for i, individual in enumerate(data):
        # Determine if the current individual is part of the filtered results
        if filtered_individuals is None or individual in filtered_individuals:
            # Insert only if it's part of the filtered results or no filter is applied
            treeview.insert("", tk.END, iid=i, values=(i+1, individual['Product Name'], individual['Product Type'], individual['Product Model'], individual['Office'], individual['Serial Number'], individual['Received by'], individual['Borrowed by'], individual['Date'], individual['Quantity']))

def open_add_dialog():
    dialog = AddItemDialog(root)

def search_treeview(event, criterion):
    query = search_entry.get().lower()
    
    if not query:  # If the search bar is empty
        populate_treeview()  # Show all items
        return

    if criterion == "Number":
        # Convert query to integer if possible
        try:
            query_number = int(query)
            filtered_individuals = [ind for i, ind in enumerate(individuals) if query_number == (i + 1)]
        except ValueError:
            # If query is not a valid integer, return empty result
            filtered_individuals = []
    else:
        # Standard search by other criteria
        filtered_individuals = [ind for ind in individuals if criterion in ind and query in str(ind[criterion]).lower()]
        
    populate_treeview(filtered_individuals)
    
def update_right_frame(content_frame, content):
    global inventory_shown
    inventory_shown = False  # Reset flag when switching content

    # Clear the existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    # Add new content based on the argument
    if content == "home":
        frame = tk.Frame(content_frame, width=RIGHT_FRAME_WIDTH, height=RIGHT_FRAME_HEIGHT)
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="Home Content", font=('Helvetica', 16)).pack(pady=20)
    elif content == "daskboard":
        frame = tk.Frame(content_frame, width=RIGHT_FRAME_WIDTH, height=RIGHT_FRAME_HEIGHT)
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="Dashboard Content", font=('Helvetica', 16)).pack(pady=20)
    elif content == "inventory":
        inventory()
    elif content == "items":
        frame = tk.Frame(content_frame, width=RIGHT_FRAME_WIDTH, height=RIGHT_FRAME_HEIGHT)
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="Items Content", font=('Helvetica', 16)).pack(pady=20)
    elif content == "profiles":
        frame = tk.Frame(content_frame, width=RIGHT_FRAME_WIDTH, height=RIGHT_FRAME_HEIGHT)
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="Profile Content", font=('Helvetica', 16)).pack(pady=20)
    elif content == "supplier":
        frame = tk.Frame(content_frame, width=RIGHT_FRAME_WIDTH, height=RIGHT_FRAME_HEIGHT)
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="Supplier Content", font=('Helvetica', 16)).pack(pady=20)
    else:
        tk.Label(content_frame, text="Default Content", font=('Helvetica', 16)).pack(pady=20)

def inventory():
    global inventory_shown
    
    if inventory_shown:
        # If inventory is already shown, just bring it to the front
        content_frame.lift()  # Bring the content_frame to the top
        return

    # Create a frame for the buttons and search section
    frame_actions = tk.Frame(content_frame)
    frame_actions.pack(side="top", padx=10, pady=5, fill=tk.X)

    # Create buttons for actions and arrange them horizontally
    btn_add = tk.Button(frame_actions, text="Add", width=8, height=2, font=('Helvetica', 9), command=open_add_dialog)
    btn_add.pack(side="left", padx=1, pady=4)

    btn_edit = tk.Button(frame_actions, text="Edit", width=8, height=2, font=('Helvetica', 9), command=edit_individual)
    btn_edit.pack(side="left", padx=1, pady=4)

    btn_delete = tk.Button(frame_actions, text="Delete", width=8, height=2, font=('Helvetica', 9), command=delete_individual)
    btn_delete.pack(side="left", padx=1, pady=4)

    # Create the search section and place it to the right of the buttons
    frame_search = tk.Frame(frame_actions)
    frame_search.pack(side="right", padx=0, pady=5)

    # Create and place search criteria label, combobox, and entry
    search_criteria_label = tk.Label(frame_search, text="Search By:", font=('Helvetica', 9))
    search_criteria_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

    search_criteria = ttk.Combobox(frame_search, values=["Number", "Product Name", "Product Type", "Product Model", "Serial Number", "Office", "Received by", "Borrowed by", "Date", "Quantity"], width=12, font=('Helvetica', 9))
    search_criteria.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    search_criteria.set("Product Name")  # Set default search criterion

    global search_entry
    search_entry = tk.Entry(frame_search, width=20, font=('Helvetica', 9))
    search_entry.grid(row=0, column=2, padx=5, pady=5, sticky='w')
    search_entry.bind("<KeyRelease>", lambda event: search_treeview(event, search_criteria.get()))  # Pass selected criterion to the search function

    # Create a frame for the Treeview widget
    frame_treeview = tk.Frame(content_frame, width=RIGHT_FRAME_WIDTH, height=RIGHT_FRAME_HEIGHT)
    frame_treeview.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
    
    # Create a Treeview widget with the "No." column
    global treeview
    treeview = ttk.Treeview(frame_treeview, columns=("No.", "Product Name", "Product Type", "Product Model", "Office", "Serial Number", "Received by", "Borrowed by", "Date", "Quantity"),
                            show="headings", selectmode="browse", height=15)
    treeview.pack(fill=tk.BOTH, expand=True)

    # Define headings for each column
    treeview.heading("No.", text="No.")
    treeview.heading("Product Name", text="Product Name")
    treeview.heading("Product Type", text="Product Type")
    treeview.heading("Product Model", text="Product Model")
    treeview.heading("Office", text="Office")
    treeview.heading("Serial Number", text="Serial Number")
    treeview.heading("Received by", text="Received by")
    treeview.heading("Borrowed by", text="Borrowed by")
    treeview.heading("Date", text="Date")
    treeview.heading("Quantity", text="Quantity")

    # Set the width of each column
    treeview.column("No.", width=40, anchor="center")
    treeview.column("Product Name", width=120, anchor="center")
    treeview.column("Product Type", width=120, anchor="center")
    treeview.column("Product Model", width=120, anchor="center")
    treeview.column("Office", width=100, anchor="center")
    treeview.column("Serial Number", width=120, anchor="center")
    treeview.column("Received by", width=120, anchor="center")
    treeview.column("Borrowed by", width=120, anchor="center")
    treeview.column("Date", width=100, anchor="center")
    treeview.column("Quantity", width=60, anchor="center")

    # Populate initial treeview data
    populate_treeview()
    
    # Set flag to indicate inventory is shown
    inventory_shown = True

def run_sys():
    global root
    global main_frame
    global content_frame
    global inventory_shown  

    root = tk.Tk()
    root.title("Inventory Management System")

    # Load and resize the image
    try:
        original_img = Image.open("logo1.png")
        img = original_img.resize((65, int(original_img.height * (65 / original_img.width))), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image: {e}")
        img = None

    # Create a main frame to hold all other frames
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create a frame for the header section
    header_section = tk.Frame(main_frame, bg='#1E90FF', height=80)
    header_section.pack(side="top", fill=tk.X)

    # Create a frame for the header content (image, title) and account button
    header_content_frame = tk.Frame(header_section, bg='#1E90FF')
    header_content_frame.pack(side="left", padx=1, pady=1)

    # Create a frame for the header text and image
    frame_header_center = tk.Frame(header_content_frame, bg='#1E90FF')
    frame_header_center.pack(side="left", fill=tk.X)

    # Place image and header in the centered frame
    if img:
        img_label = tk.Label(frame_header_center, image=img, bg='#1E90FF')
        img_label.pack(side="left", padx=(40, 10), pady=5)  # Increase the left padding for the image

    header_label = tk.Label(frame_header_center, text="Inventory Management System", font=('Helvetica', 25, 'bold'), bg='#1E90FF', fg='white')
    header_label.pack(side="left", padx=0, pady=10)

    try:
        user_img = Image.open("user.png")
        user_img = user_img.resize((50, int(user_img.height * (50 / user_img.width))), Image.Resampling.LANCZOS)
        user_img = ImageTk.PhotoImage(user_img)
    except Exception as e:
        print(f"Error loading user image: {e}")
        user_img = None
    
    user_img_button = tk.Button(header_section, image=user_img, bg='#1E90FF', borderwidth=0, command=lambda: print("User image clicked!"))
    user_img_button.pack(side="right", padx=(20, 30), pady=5)
    
    # Create a frame for the sidebar with a raised border
    sidebar = tk.Frame(main_frame, width=200, bg='#f0f0f0', relief='raised')
    sidebar.pack(side="left", fill=tk.Y, pady=(5, 0))  # Adjust padding to be below the header

    # Create a frame for headers in the sidebar
    sidebar_content_frame = tk.Frame(sidebar, bg='#f0f0f0')
    sidebar_content_frame.pack(fill=tk.X, pady=(1, 0))  # Adjust top padding

    def create_sidebar_button(text, content):
        return tk.Button(sidebar_content_frame, text=text, width=17, height=2, relief='flat', bg='#f0f0f0', font=('Helvetica', 12),
                        command=lambda: update_right_frame(content_frame, content) if content != "inventory" else inventory())

    # Create sidebar buttons with consistent sizing
    create_sidebar_button("Home", "home").pack(fill='x', pady=(5, 0))
    create_sidebar_button("Dashboard", "dashboard").pack(fill='x', pady=(5, 0))
    create_sidebar_button("Inventory", "inventory").pack(fill='x', pady=(5, 0))
    create_sidebar_button("Items", "items").pack(fill='x', pady=(5, 0))
    create_sidebar_button("Profiles", "profiles").pack(fill='x', pady=(5, 0))
    create_sidebar_button("Supplier", "supplier").pack(fill='x', pady=(5, 0))

    # Create a frame for the content area below the header
    content_frame = tk.Frame(main_frame)
    content_frame.pack(side="top", fill=tk.BOTH, expand=True)

    # Initialize inventory_shown
    inventory_shown = False

    # Run the tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    run_sys()
