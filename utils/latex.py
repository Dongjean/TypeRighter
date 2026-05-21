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

def GET_latex_window(output_frame, latex_str, background_color):
    
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
            canvas = tk.Canvas(
                output_frame,
                width=img.width,
                height=img.height,
                bg=background_color,
                highlightthickness=0,
            )
            canvas.pack(expand=True)
            canvas.create_image(img.width // 2, img.height // 2, image=tk_img)

            canvas.image = tk_img
        else:
            tk.Label(output_frame, text="API Error: Could not render image.", bg="white").pack(expand=True)
    
    except Exception as e:
        tk.Label(output_frame, text=f"{e}", bg=background_color).pack(expand=True)