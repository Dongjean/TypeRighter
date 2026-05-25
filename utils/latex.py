# Local matplotlib LaTeX method

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def init_latex_window_matplotlib(output_frame, background_color):
    
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

def display_latex_window_matplotlib(equation, background_color, canvas, ax):
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

# API LaTeX method
  
import tkinter as tk
import requests
from io import BytesIO
from PIL import Image, ImageTk

def color_to_transparent(convert_color, img):
    
    TR = convert_color[0]
    TG = convert_color[1]
    TB = convert_color[2]
    
    # Express each pixel's data as [(R, G, B, A), ...]
    pixels = img.getdata()
    new_pixels = []
    for i in range(len(pixels)):
        pixel = pixels[i]
        # If the pixel is pure white (or very close to it), make it completely transparent
        R = pixel[0]
        G = pixel[1]
        B = pixel[2]
        if R == TR and G == TG and B == TB:
            # Add a new pixel where the Alpha channel is 0 (transparent pixel)
            new_pixels.append((0, 0, 0, 0))
        else:
            # Otherwise the pixel isnt to be removed
            new_pixels.append(pixel)
    img.putdata(new_pixels)

def init_latex_window_codecogs(output_frame, background_color):
    canvas = tk.Canvas(
        output_frame,
        bg=background_color,
        highlightthickness=0,
    )
    canvas.pack(fill="both", expand=True)

    return canvas

def display_latex_window_codecogs(canvas, latex_str):
    
    # CodeCogs LaTeX rendering API
    url = fr"https://latex.codecogs.com/png.image?\dpi{{150}}{latex_str}"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            
            # Add the alpha channel
            # NOTE: CodeCogs doesnt return with alpha channel, so this alpha channel is all 255
            img = Image.open(BytesIO(response.content)).convert("RGBA")

            # Convert all white pixels in img to transparent
            color_to_transparent((255, 255, 255), img)

            # Render this on a tkinter canvas on the given output frame
            tk_img = ImageTk.PhotoImage(img)
            
            canvas.config(width=img.width, height=img.height)
            canvas.create_image(img.width // 2, img.height // 2, image=tk_img)

            canvas.image = tk_img
        else:
            print("API Error: Could not render image.")
    
    except Exception as e:
        print(e)