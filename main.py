import pyautogui
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import simpledialog
import os

# Function to take a screenshot and save it
def take_screenshot(file_path):
    screenshot = pyautogui.screenshot()
    screenshot.save(file_path)

# Function to crop the image using a GUI
def crop_image(file_path):
    # Load the image
    image = Image.open(file_path)

    # Create a tkinter window
    root = tk.Tk()
    root.title("Crop Image")

    # Convert the image to a format tkinter can use
    tk_image = ImageTk.PhotoImage(image)

    # Create a canvas and put the image on it
    canvas = tk.Canvas(root, width=image.width, height=image.height)
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
            # Crop the image
            left = min(start_x, end_x)
            top = min(start_y, end_y)
            right = max(start_x, end_x)
            bottom = max(start_y, end_y)
            cropped_image = image.crop((left, top, right, bottom))
            cropped_image.save(file_path)
            root.destroy()

    # Bind mouse events to the canvas
    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    root.mainloop()

# Define file path
file_path = "board.png"

# Take screenshot
take_screenshot(file_path)

# Crop image
crop_image(file_path)
