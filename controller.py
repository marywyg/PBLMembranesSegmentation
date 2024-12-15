from model import ImageModel
from view import ImageView
import os
from tkinter import filedialog
class ImageController:
    def __init__(self, root):
        self.model = ImageModel()
        self.view = ImageView(root)

        # Ustawienie callbacków
        self.view.set_load_button_callback(self.load_image)
        self.view.set_blur_button_callback(self.apply_blur)
        self.view.set_sharpen_button_callback(self.apply_sharpen)
        self.view.set_edge_button_callback(self.apply_edge_enhancement)
        self.view.set_otsu_button_callback(self.apply_otsu_threshold)
        self.view.set_save_button_callback(self.save_image)  # Ustawienie callbacku dla przycisku zapisu
        self.view.fuzzy_button.config(command=self.apply_fuzzy_c_means)

    def load_image(self):

        file_path = self.view.get_image_path()
        if file_path:
            self.model.load_image(file_path)
            self.view.show_image(self.model.get_image())
        else:
            self.view.show_error("Nie wybrano obrazu!")

    def apply_blur(self):

        if self.model.get_image():
            blurred_image = self.model.apply_blur()
            if blurred_image:
                self.view.show_image(blurred_image)
        else:
            self.view.show_error("Najpierw wczytaj obraz.")

    def apply_sharpen(self):

        if self.model.get_image():
            sharpened_image = self.model.apply_sharpen()
            if sharpened_image:
                self.view.show_image(sharpened_image)
        else:
            self.view.show_error("Najpierw wczytaj obraz.")

    def apply_otsu_threshold(self):
        if self.model.get_image():
            otsu_applied_image = self.model.apply_otsu_threshold()
            if otsu_applied_image:
                self.view.show_image(otsu_applied_image)
        else:
            self.view.show_error("Najpierw wczytaj obraz.")
    def apply_edge_enhancement(self):

        if self.model.get_image():
            edge_enhanced_image = self.model.apply_edge_enhancement()
            if edge_enhanced_image:
                self.view.show_image(edge_enhanced_image)
        else:
            self.view.show_error("Najpierw wczytaj obraz.")
            
    def apply_fuzzy_c_means(self):
        if self.model.get_image():
            fuzzy_image = self.model.apply_fuzzy_c_means(n_clusters=3)
            if fuzzy_image:
                self.view.show_image(fuzzy_image)
        else:
            self.view.show_error("Najpierw wczytaj obraz.")
            
    def save_image(self):

        if self.model.get_image():
            # Sprawdź, czy folder 'results' istnieje, jeśli nie, to go utwórz
            results_folder = os.path.join(os.getcwd(), "results")
            if not os.path.exists(results_folder):
                os.makedirs(results_folder)
    
            # Otwórz okno dialogowe do zapisania pliku w folderze 'results'
            file_path = filedialog.asksaveasfilename(
                initialdir=results_folder,  # Początkowy katalog to 'results'
                defaultextension=".tiff", 
                filetypes=[("TIFF files", "*.tiff;*.tif")]
            )

            if file_path:
                # Zapisz obraz w oryginalnym rozmiarze w folderze 'results'
                self.model.get_image().save(file_path)
        else:
            self.view.show_error("Nie ma obrazu do zapisania!")
    

