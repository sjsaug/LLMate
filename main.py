import mss
from PIL import Image, ImageTk
import tkinter as tk
import os

# Function to take a screenshot and save it
def take_screenshot(file_path):
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Capture the primary monitor
        screenshot = sct.grab(monitor)
        img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
        print(f"Screenshot size: {img.size}")  # Debug print to check the size of the screenshot
        img.save(file_path)

# Function to crop the image using a GUI
def crop_image(file_path):
    # Load the image
    image = Image.open(file_path)
    print(f"Loaded image size: {image.size}")  # Debug print to check the size of the loaded image

    # Create a tkinter window
    root = tk.Tk()
    root.title("Crop Image")

    # Resize the image to fit the screen if necessary
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    print(f"Screen size: {screen_width}x{screen_height}")  # Debug print to check the screen size

    if image.width > screen_width or image.height > screen_height:
        scale = min(screen_width / image.width, screen_height / image.height)
        resized_image = image.resize((int(image.width * scale), int(image.height * scale)), Image.ANTIALIAS)
    else:
        resized_image = image

    # Convert the image to a format tkinter can use
    tk_image = ImageTk.PhotoImage(resized_image)
    print(f"Tkinter image size: {tk_image.width()}x{tk_image.height()}")  # Debug print to check the size of the Tkinter image

    # Create a canvas to display the image
    canvas = tk.Canvas(root, width=tk_image.width(), height=tk_image.height())
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    # Variables to store the coordinates of the crop box
    start_x = start_y = end_x = end_y = None

    # Mouse event handlers
    def on_button_press(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y

    def on_mouse_drag(event):
        nonlocal end_x, end_y
        end_x, end_y = event.x, event.y
        canvas.delete("crop_box")
        canvas.create_rectangle(start_x, start_y, end_x, end_y, outline="red", tags="crop_box")

    def on_button_release(event):
        nonlocal start_x, start_y, end_x, end_y
        end_x, end_y = event.x, event.y
        if start_x and start_y and end_x and end_y:
            crop_box = (start_x, start_y, end_x, end_y)
            cropped_image = resized_image.crop(crop_box)
            cropped_image.save("board_" + os.path.basename(file_path))
            print(f"Cropped image saved as cropped_{os.path.basename(file_path)}")

    # Bind the mouse events to the canvas
    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    root.mainloop()

# Example usage
file_path = "display.png"
take_screenshot(file_path)
crop_image(file_path)