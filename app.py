from datetime import datetime
import tkinter as tk

# Create the window
root = tk.Tk()
root.title("Transparent Timer")

# Window Customization
win_w, win_h = 300, 150
root.geometry(f"{win_w}x{win_h}")
root.attributes('-alpha', 1.0)
root.overrideredirect(True)  # Remove window decorations
root.wm_attributes("-topmost", True)  # Keep on top

# Set transparency
transparent_color = 'black'
root.config(bg=transparent_color)
root.wm_attributes('-transparentcolor', transparent_color)

# Create the label to display the time
label = tk.Label(
    root,
    font=("calibri", 20, "bold"),
    bg=transparent_color,
    fg="white",
    text="",
)
label.pack(expand=True, fill="both")

# Create the invisible hitbox (behind the timer)
hitbox = tk.Frame(root, bg="#010101")  # Invisible hitbox (almost black)
hitbox.pack(expand=True, fill="both")
hitbox.lower()  # Send it to the back, behind the label

# Function to adjust the hitbox size to match the label
def resize_hitbox(event=None):
    label_width = label.winfo_width()
    label_height = label.winfo_height()
    
    # Adjust the hitbox size to match the label size
    hitbox.config(width=label_width, height=label_height)
    hitbox.place(x=label.winfo_x(), y=label.winfo_y())

# Call resize_hitbox after the window and label are packed
root.after(100, resize_hitbox)  # Delay to allow window size calculation

# Setting up the time components
def clock():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    label.config(text=f"{date}\n{time}")
    label.after(1000, clock)  # Update the time every 1000ms (1 second)

# Start the clock
clock()

# Function for moving the window around
def start_drag(event):
    root._dx, root._dy = event.x_root, event.y_root

def on_drag(event):
    x = root.winfo_x() + event.x_root - root._dx
    y = root.winfo_y() + event.y_root - root._dy
    root.geometry(f"+{x}+{y}")
    root._dx, root._dy = event.x_root, event.y_root

# Create the tab bar (it will only show when hovering over the timer)
tab_bar = tk.Frame(root, bg="gray20", height=30)

tab1 = tk.Label(tab_bar, text="Timer", bg="gray30", fg="white", padx=10, pady=5)
tab2 = tk.Label(tab_bar, text="Other", bg="gray20", fg="white", padx=10, pady=5)

tab1.pack(side="left")
tab2.pack(side="left")

# Function to show/hide tab bar based on hover
def hover_check():
    px, py = root.winfo_pointerxy()  # Get current mouse position
    rx, ry = root.winfo_rootx(), root.winfo_rooty()  # Get the window position
    label_w, label_h = label.winfo_width(), label.winfo_height()

    # Check if mouse is over the label
    inside_label = rx <= px <= rx + label_w and ry <= py <= ry + label_h

    # Show or hide the tab bar based on the hover
    if inside_label:
        if not tab_bar.winfo_ismapped():
            tab_bar.place(x=0, y=0, relwidth=1)  # Place tab bar at the top
    else:
        tab_bar.place_forget()  # Hide tab bar when not hovering over the timer

    root.after(80, hover_check)  # Repeat the check every 80ms

# Start the hover check loop
hover_check()

# Start the drag behavior on the tab bar
tab_bar.bind("<Button-1>", start_drag)
tab_bar.bind("<B1-Motion>", on_drag)

# Run the Tkinter event loop
root.mainloop()
