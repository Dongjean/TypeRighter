from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def init_latex_window(output_frame, background_color):
    
    # Create a Matplotlib figure and axis to hold LaTeX output
    fig, ax = plt.subplots(figsize=(5, 2), facecolor=background_color)
    ax.axis('off')  # Hide the default plot axes, grid, and borders

    # Middleman hybrid wrapper for matplotlib figures and tkinter widgets
    # This is a matplotlib object
    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    # Render the canvas on matplotlib's side
    canvas.draw()

    # Extract the underlying tkinter widget from the FigureCanvasTkAgg() object
    canvas_widget = canvas.get_tk_widget()
    # Render the canvas on tkinter's side
    canvas_widget.pack(fill="both", expand=True)

    return ax, canvas

def display_latex_window(equation, background_color, canvas, ax):
  try:
    # Clear all existing text
    ax.clear()
    ax.axis('off')

    # The LaTeX output on the figure
    # equation = r'$\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$'
    ax.text(0.5, 0.5, equation, size=24, ha='center', va='center')

    canvas.draw_idle()
  except Exception as e:
    print(f'error displaying latex: {e}')