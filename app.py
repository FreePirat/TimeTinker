from datetime import datetime
import tkinter as tk

# To create the window itself
root = tk.Tk()
root.title("Transparent Timer")

# Window Customization
root.geometry("200x100")
root.attributes('-alpha', 0.0) 
root.overrideredirect(True)  # Remove window decorations

# Create a label to display the time
label = tk.Label(root, font=("calibri", 40, "bold"), background="black", foreground="white")
label.pack(anchor="center")

# Setting up the time components
def clock():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    timewithMil = now.strftime("%H:%M:%S.%f")
    label.config(text=f"{date}\n{time}\n{timewithMil}")
    label.after(1000, clock)  # Update the time every 1000ms (1 second)

# Starting the clock function
clock()

# Run the Tkinter event loop
root.mainloop()