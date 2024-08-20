from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title('Login')
root.configure(bg="#fff")
root.resizable(False, False)

# Calculate the position to center the window
window_width = 925
window_height = 500

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates to center the window
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the geometry of the window
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Open and resize the image
original_image = Image.open('logo1.png')
resized_image = original_image.resize((300, 300))  # Adjust size as needed
img = ImageTk.PhotoImage(resized_image)

# Add a Label widget to display the image
image_label = Label(root, image=img, bg='white')
image_label.place(x=100, y=100)  # Adjust the position as needed

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='Sign In', fg='#57a1f8', bg='white', font=('Microsoft TaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

##################-----------------------------------
user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft TaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, "Username")

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

##################-----------------------------------
code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft TaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

#################################################

Button(frame, width=39, pady=7, text='Sign In', bg='#57a1f8', fg='white', border=0).place(x=35, y=204)

sign_up= Button(frame, width=17, text='Open as Spectator', border=0, bg='white', cursor='hand2', fg='#57a1f8')
sign_up.place(x=120, y=270)



root.mainloop()
