from datetime import datetime
import tkinter as tk
from tkinter import ttk, colorchooser, font, messagebox
import json
import os

# Default settings
DEFAULT_SETTINGS = {
    'font_family': 'Calibri',
    'font_size': 20,
    'font_weight': 'bold',
    'text_color': 'white',
    'bg_color': 'black',
    'transparency': 1.0,
    'time_format': '24h',  # '12h' or '24h'
    'show_date': True,
    'show_seconds': True,
    'date_format': '%Y-%m-%d',  # Default date format
    'window_width': 300,
    'window_height': 150
}

# Load settings from file
def load_settings():
    try:
        if os.path.exists('clock_settings.json'):
            with open('clock_settings.json', 'r') as f:
                settings = json.load(f)
                # Merge with defaults to ensure all keys exist
                return {**DEFAULT_SETTINGS, **settings}
    except Exception as e:
        print(f"Error loading settings: {e}")
    return DEFAULT_SETTINGS.copy()

# Save settings to file
def save_settings():
    try:
        with open('clock_settings.json', 'w') as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"Error saving settings: {e}")

# Initialize settings
settings = load_settings()

# Create the window
root = tk.Tk()
root.title("TimeTinker - Customizable Digital Clock")

# Window Customization
win_w, win_h = settings['window_width'], settings['window_height']
root.geometry(f"{win_w}x{win_h}")
root.attributes('-alpha', settings['transparency'])
root.overrideredirect(True)  # Remove window decorations
root.wm_attributes("-topmost", True)  # Keep on top

# Set transparency
transparent_color = settings['bg_color']
root.config(bg=transparent_color)
root.wm_attributes('-transparentcolor', transparent_color)

# Create the label to display the time
label = tk.Label(
    root,
    font=(settings['font_family'], settings['font_size'], settings['font_weight']),
    bg=transparent_color,
    fg=settings['text_color'],
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
    
    # Format date if enabled
    date_str = ""
    if settings['show_date']:
        date_str = now.strftime(settings['date_format'])
    
    # Format time based on 12h/24h preference
    if settings['time_format'] == '12h':
        if settings['show_seconds']:
            time_str = now.strftime("%I:%M:%S %p")
        else:
            time_str = now.strftime("%I:%M %p")
    else:  # 24h format
        if settings['show_seconds']:
            time_str = now.strftime("%H:%M:%S")
        else:
            time_str = now.strftime("%H:%M")
    
    # Combine date and time
    if date_str and time_str:
        display_text = f"{date_str}\n{time_str}"
    elif date_str:
        display_text = date_str
    else:
        display_text = time_str
    
    label.config(text=display_text)
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

# Function to update clock appearance
def update_clock_appearance():
    # Update label font and colors
    label.config(
        font=(settings['font_family'], settings['font_size'], settings['font_weight']),
        fg=settings['text_color'],
        bg=settings['bg_color']
    )
    
    # Update window properties
    root.config(bg=settings['bg_color'])
    root.wm_attributes('-transparentcolor', settings['bg_color'])
    root.attributes('-alpha', settings['transparency'])
    
    # Update window size
    root.geometry(f"{settings['window_width']}x{settings['window_height']}")

# Settings window
def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Clock Settings")
    settings_window.geometry("500x600")
    settings_window.resizable(False, False)
    settings_window.attributes('-topmost', True)
    
    # Create notebook for tabs
    notebook = ttk.Notebook(settings_window)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Appearance tab
    appearance_frame = ttk.Frame(notebook)
    notebook.add(appearance_frame, text="Appearance")
    
    # Font settings
    font_frame = ttk.LabelFrame(appearance_frame, text="Font", padding="10")
    font_frame.pack(fill="x", pady=5)
    
    # Font family
    ttk.Label(font_frame, text="Font Family:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    font_var = tk.StringVar(value=settings['font_family'])
    font_combo = ttk.Combobox(font_frame, textvariable=font_var, values=list(font.families()))
    font_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
    
    # Font size
    ttk.Label(font_frame, text="Font Size:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    size_var = tk.IntVar(value=settings['font_size'])
    size_spin = ttk.Spinbox(font_frame, from_=8, to=72, textvariable=size_var)
    size_spin.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
    
    # Font weight
    ttk.Label(font_frame, text="Font Weight:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
    weight_var = tk.StringVar(value=settings['font_weight'])
    weight_combo = ttk.Combobox(font_frame, textvariable=weight_var, values=['normal', 'bold'])
    weight_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
    
    font_frame.columnconfigure(1, weight=1)
    
    # Color settings
    color_frame = ttk.LabelFrame(appearance_frame, text="Colors", padding="10")
    color_frame.pack(fill="x", pady=5)
    
    def choose_text_color():
        color = colorchooser.askcolor(color=settings['text_color'])[1]
        if color:
            settings['text_color'] = color
            text_color_btn.config(bg=color)
    
    def choose_bg_color():
        color = colorchooser.askcolor(color=settings['bg_color'])[1]
        if color:
            settings['bg_color'] = color
            bg_color_btn.config(bg=color)
    
    ttk.Label(color_frame, text="Text Color:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    text_color_btn = tk.Button(color_frame, bg=settings['text_color'], width=10, command=choose_text_color)
    text_color_btn.grid(row=0, column=1, padx=5, pady=2)
    
    ttk.Label(color_frame, text="Background Color:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    bg_color_btn = tk.Button(color_frame, bg=settings['bg_color'], width=10, command=choose_bg_color)
    bg_color_btn.grid(row=1, column=1, padx=5, pady=2)
    
    # Transparency
    ttk.Label(color_frame, text="Transparency:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
    transparency_var = tk.DoubleVar(value=settings['transparency'])
    transparency_scale = ttk.Scale(color_frame, from_=0.1, to=1.0, variable=transparency_var, orient="horizontal")
    transparency_scale.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
    
    color_frame.columnconfigure(1, weight=1)
    
    # Window size
    size_frame = ttk.LabelFrame(appearance_frame, text="Window Size", padding="10")
    size_frame.pack(fill="x", pady=5)
    
    ttk.Label(size_frame, text="Width:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    width_var = tk.IntVar(value=settings['window_width'])
    width_spin = ttk.Spinbox(size_frame, from_=200, to=800, textvariable=width_var)
    width_spin.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
    
    ttk.Label(size_frame, text="Height:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    height_var = tk.IntVar(value=settings['window_height'])
    height_spin = ttk.Spinbox(size_frame, from_=100, to=400, textvariable=height_var)
    height_spin.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
    
    size_frame.columnconfigure(1, weight=1)
    
    # Time Format tab
    format_frame = ttk.Frame(notebook)
    notebook.add(format_frame, text="Time Format")
    
    # Time format options
    time_format_frame = ttk.LabelFrame(format_frame, text="Time Format", padding="10")
    time_format_frame.pack(fill="x", pady=5)
    
    time_format_var = tk.StringVar(value=settings['time_format'])
    ttk.Radiobutton(time_format_frame, text="12 Hour (AM/PM)", variable=time_format_var, value="12h").pack(anchor="w")
    ttk.Radiobutton(time_format_frame, text="24 Hour", variable=time_format_var, value="24h").pack(anchor="w")
    
    # Display options
    display_frame = ttk.LabelFrame(format_frame, text="Display Options", padding="10")
    display_frame.pack(fill="x", pady=5)
    
    show_date_var = tk.BooleanVar(value=settings['show_date'])
    ttk.Checkbutton(display_frame, text="Show Date", variable=show_date_var).pack(anchor="w")
    
    show_seconds_var = tk.BooleanVar(value=settings['show_seconds'])
    ttk.Checkbutton(display_frame, text="Show Seconds", variable=show_seconds_var).pack(anchor="w")
    
    # Date format
    date_format_frame = ttk.LabelFrame(format_frame, text="Date Format", padding="10")
    date_format_frame.pack(fill="x", pady=5)
    
    ttk.Label(date_format_frame, text="Format:").pack(anchor="w")
    date_format_var = tk.StringVar(value=settings['date_format'])
    date_format_combo = ttk.Combobox(date_format_frame, textvariable=date_format_var, values=[
        '%Y-%m-%d',      # 2023-12-25
        '%d/%m/%Y',      # 25/12/2023
        '%m/%d/%Y',      # 12/25/2023
        '%B %d, %Y',     # December 25, 2023
        '%d %B %Y',      # 25 December 2023
        '%a, %d %b %Y'   # Mon, 25 Dec 2023
    ])
    date_format_combo.pack(fill="x", pady=2)
    
    # Buttons
    button_frame = ttk.Frame(settings_window)
    button_frame.pack(fill="x", padx=10, pady=10)
    
    def apply_settings():
        # Update settings
        settings['font_family'] = font_var.get()
        settings['font_size'] = size_var.get()
        settings['font_weight'] = weight_var.get()
        settings['transparency'] = transparency_var.get()
        settings['window_width'] = width_var.get()
        settings['window_height'] = height_var.get()
        settings['time_format'] = time_format_var.get()
        settings['show_date'] = show_date_var.get()
        settings['show_seconds'] = show_seconds_var.get()
        settings['date_format'] = date_format_var.get()
        
        # Apply changes
        update_clock_appearance()
        save_settings()
        
        messagebox.showinfo("Settings", "Settings applied successfully!")
    
    def reset_settings():
        global settings
        settings = DEFAULT_SETTINGS.copy()
        update_clock_appearance()
        save_settings()
        settings_window.destroy()
        messagebox.showinfo("Settings", "Settings reset to defaults!")
    
    ttk.Button(button_frame, text="Apply", command=apply_settings).pack(side="right", padx=5)
    ttk.Button(button_frame, text="Reset to Defaults", command=reset_settings).pack(side="right", padx=5)
    ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side="right", padx=5)

# Create the tab bar (it will only show when hovering over the timer)
tab_bar = tk.Frame(root, bg="gray20", height=30)

# Create tabs with functionality
def close_app():
    save_settings()
    root.quit()

tab_settings = tk.Label(tab_bar, text="Settings", bg="gray30", fg="white", padx=10, pady=5, cursor="hand2")
tab_close = tk.Label(tab_bar, text="X", bg="gray20", fg="white", padx=10, pady=5, cursor="hand2")

# Bind click events
tab_settings.bind("<Button-1>", lambda e: open_settings())
tab_close.bind("<Button-1>", lambda e: close_app())

# Add hover effects
def on_enter(event, widget):
    widget.config(bg="gray40")

def on_leave(event, widget):
    original_bg = "gray30" if widget == tab_settings else "gray20"
    widget.config(bg=original_bg)

tab_settings.bind("<Enter>", lambda e: on_enter(e, tab_settings))
tab_settings.bind("<Leave>", lambda e: on_leave(e, tab_settings))
tab_close.bind("<Enter>", lambda e: on_enter(e, tab_close))
tab_close.bind("<Leave>", lambda e: on_leave(e, tab_close))

tab_settings.pack(side="left")
tab_close.pack(side="left")

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

# Create context menu
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Settings", command=open_settings)
context_menu.add_separator()
context_menu.add_command(label="Reset Position", command=lambda: root.geometry(f"{settings['window_width']}x{settings['window_height']}+100+100"))
context_menu.add_separator()
context_menu.add_command(label="Close", command=close_app)

def show_context_menu(event):
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()

# Bind right-click to show context menu
label.bind("<Button-3>", show_context_menu)

# Save settings on close
root.protocol("WM_DELETE_WINDOW", close_app)

# Run the Tkinter event loop
root.mainloop()
