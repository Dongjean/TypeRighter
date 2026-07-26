# Local matplotlib LaTeX method

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from urllib.parse import quote

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
import win32clipboard as clip
import win32con
from io import BytesIO

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
        name="latex_output_canvas"
    )
    canvas.pack(expand=True)

    return canvas

def display_latex_window_codecogs(canvas, latex_str):
    
    # CodeCogs LaTeX rendering API
    url = "https://latex.codecogs.com/png.image?" + quote(r"\dpi{150}" +latex_str, safe="")

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
            
            # We need this reference to tk_img to signal to Python that we still need this variable
            # This prevents Python from clearing tk_img from memory after we stop referencing it directly, allowing us to render it
            canvas.image = tk_img

            # Save the PIL image so we can copy to clipboard later
            canvas.pil_img = img
        else:
            print("API Error: Could not render image.")
    
    except Exception as e:
        print(e)

def copy_canvas_image(canvas):

    # Access the PIL image
    img = getattr(canvas, "pil_img", None)
    if img is None: 
        return

    # Convert the image to RGBA just in case
    rgba_img = img.convert("RGBA")

    # Copy this RGBA image to a bytes stream, output, in BMP format
    output = BytesIO()
    rgba_img.save(output, "BMP")

    # BPP images are just DIB images with a 14-byte header
    # Slice out this 14-byte header to extract the DIB image data
    dib_data = output.getvalue()[14:]

    # Slicing a BytesIO() object creates a copy of it
    # We can close the original BytesIO() object
    output.close()

    # Copy the image data in dib_data to clipboard
    clip.OpenClipboard()
    try:
        clip.EmptyClipboard()
        # win32con.CF_DIB is a windows-specific constant which identifies the DIB image format
        clip.SetClipboardData(win32con.CF_DIB, dib_data)
    finally:
        clip.CloseClipboard()