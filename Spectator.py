import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

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
    for i, individual in enumerate(individuals):
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

def run_app():
    global root
    root = tk.Tk()
    root.title("Inventory Management")

    # Create a frame for the buttons
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

    # Create buttons with specific width, height, and font size
    btn_add = tk.Button(frame_buttons, text="Add", width=10, height=2, font=('Helvetica', 9), command=open_add_dialog)
    btn_add.grid(row=0, column=0, padx=5, pady=5)

    btn_edit = tk.Button(frame_buttons, text="Edit", width=10, height=2, font=('Helvetica', 9), command=edit_individual)
    btn_edit.grid(row=0, column=1, padx=5, pady=5)

    btn_delete = tk.Button(frame_buttons, text="Delete", width=10, height=2, font=('Helvetica', 9), command=delete_individual)
    btn_delete.grid(row=0, column=2, padx=5, pady=5)

    # Create and pack a search section to the right of the buttons
    frame_search = tk.Frame(root)
    frame_search.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

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
    frame_treeview = tk.Frame(root)
    frame_treeview.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

    # Create and pack Treeview widget
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

    # Run the tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    run_app()
