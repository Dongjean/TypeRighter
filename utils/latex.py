from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk

def display_latex_window(output_frame, equation, background_color):
  try:
    
    # Close all existing matplotlib figures
    plt.close('all')

    # Close all existing canvases
    for widget in output_frame.winfo_children():
      if isinstance(widget, tk.Canvas):
        widget.destroy()
    
    # Create a Matplotlib figure and axis to hold LaTeX output
    fig, ax = plt.subplots(figsize=(5, 2), facecolor=background_color)
    ax.axis('off')  # Hide the default plot axes, grid, and borders

    # The LaTeX output on the figure
    # equation = r'$\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$'
    ax.text(0.5, 0.5, equation, size=24, ha='center', va='center')

    # Middleman hybrid wrapper for matplotlib figures and tkinter widgets
    # This is a matplotlib object
    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    # Render the canvas on matplotlib's side
    canvas.draw()

    # Extract the underlying tkinter widget from the FigureCanvasTkAgg() object
    canvas_widget = canvas.get_tk_widget()
    # Render the canvas on tkinter's side
    canvas_widget.pack(fill="both", expand=True)
  except Exception as e:
    plt.close('all')
    print(f'error displaying latex: {e}')