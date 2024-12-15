import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk

class ImageView:
    def __init__(self, root):
        self.root = root
        self.root.title("Segmentacja membran")

        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()

        self.load_button = tk.Button(root, text="Wczytaj obraz")
        self.load_button.pack()

        self.blur_button = tk.Button(root, text="Blur")
        self.blur_button.pack()

        self.sharpen_button = tk.Button(root, text="Sharpen")
        self.sharpen_button.pack()

        self.edge_button = tk.Button(root, text="Edge Enhancement")
        self.edge_button.pack()
        
        self.otsu_button = tk.Button(root, text="Otsu")
        self.otsu_button.pack()
        
        self.fuzzy_button = tk.Button(root, text="Fuzzy C-Means")
        self.fuzzy_button.pack()
        
        self.save_button = tk.Button(root, text="Zapisz obraz")
        self.save_button.pack()
        
        

    
    def show_image(self, image):
    
        max_width = self.canvas.winfo_width()
        max_height = self.canvas.winfo_height()
        
        display_image = image.copy()

        image_width, image_height = image.size
        scale = min(max_width / image_width, max_height / image_height)
    
        new_width = int(image_width * scale)
        new_height = int(image_height * scale)
        resized_image = display_image.resize((new_width, new_height))

        x_center = (max_width - new_width) // 2
        y_center = (max_height - new_height) // 2

        photo = ImageTk.PhotoImage(resized_image)

        self.canvas.create_image(x_center, y_center, image=photo, anchor=tk.NW)
        self.canvas.image = photo 


    def show_error(self, message):
        messagebox.showwarning("Błąd", message)

    def get_image_path(self):

        return filedialog.askopenfilename(filetypes=[("TIFF files", "*.tiff;*.tif")])

    def set_load_button_callback(self, callback):

        self.load_button.config(command=callback)

    def set_blur_button_callback(self, callback):

        self.blur_button.config(command=callback)

    def set_sharpen_button_callback(self, callback):

        self.sharpen_button.config(command=callback)

    def set_edge_button_callback(self, callback):

        self.edge_button.config(command=callback)
        
    def set_otsu_button_callback(self, callback):
        
        self.otsu_button.config(command=callback)
        
    def set_save_button_callback(self, callback):

        self.save_button.config(command=callback)
        
    def set_fuzzy_button_callback(self, callback):

        self.fuzzy_button.config(command=callback)