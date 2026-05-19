import tkinter as tk

def alert_window(alert_title, alert_message):
    # We create a temporary hidden window so the messagebox has a parent
    root = tk.Tk()
    root.withdraw()  # Hide the main tiny Tkinter window
    root.attributes("-topmost", True) # Force it to the front
    
    # This creates the actual "Window" popup
    tk.messagebox.showinfo(alert_title, alert_message)
    
    root.destroy() # Clean up memory after you click 'OK'