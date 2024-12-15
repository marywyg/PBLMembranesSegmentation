from PIL import Image, ImageFilter, ImageOps
from tkinter import messagebox
import cv2
import numpy as np
import skfuzzy as fuzz
class ImageModel:
    def __init__(self):
        self.image = None  
        self.image_path = None  

    def load_image(self, file_path):

        try:
            self.image_path = file_path
            self.image = Image.open(file_path)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać obrazu: {e}")

    def apply_blur(self):

        if self.image:
            self.image = self.image.filter(ImageFilter.GaussianBlur(radius=3))  # Mocniejsze rozmycie
            return self.image
        else:
            messagebox.showwarning("Błąd", "Najpierw wczytaj obraz.")
            return None

    def apply_sharpen(self):

        if self.image:
            self.image = self.image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
            return self.image
        else:
            messagebox.showwarning("Błąd", "Najpierw wczytaj obraz.")
            return None

    def apply_edge_enhancement(self):

        if self.image:
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            return self.image
        else:
            messagebox.showwarning("Błąd", "Najpierw wczytaj obraz.")
            return None
    
    def apply_otsu_threshold(self):
        if self.image:
            # Konwersja obrazu do skali szarości
            grayscale_image = ImageOps.grayscale(self.image)
            image_np = np.array(grayscale_image)

            # Histogram i metoda Otsu
            histogram, _ = np.histogram(image_np, bins=256, range=(0, 256))
            total_pixels = image_np.size

            max_variance = 0
            optimal_threshold = 0
            sum_total = np.dot(np.arange(256), histogram)
            sum_background = 0
            weight_background = 0

            for t in range(256):
                weight_background += histogram[t]
                if weight_background == 0:
                    continue
                weight_foreground = total_pixels - weight_background
                if weight_foreground == 0:
                    break
                sum_background += t * histogram[t]
                mean_background = sum_background / weight_background
                mean_foreground = (sum_total - sum_background) / weight_foreground
                variance_between = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2
                if variance_between > max_variance:
                    max_variance = variance_between
                    optimal_threshold = t

            # Zastosowanie progu
            binary_image = (image_np > optimal_threshold).astype(np.uint8) * 255
            self.image = Image.fromarray(binary_image)
            return self.image
        else:
            messagebox.showwarning("Błąd", "Najpierw wczytaj obraz.")
            return None

    def get_image(self):

        return self.image
    
    def save_image(self):

        if self.model.get_image():
            file_path = filedialog.asksaveasfilename(defaultextension=".tiff", filetypes=[("TIFF files", "*.tiff;*.tif")])
            if file_path:
                # Zapisz obraz w oryginalnym rozmiarze
                self.model.get_image().save(file_path)
        else:
            self.view.show_error("Nie ma obrazu do zapisania!")
    
    def apply_fuzzy_c_means(self, n_clusters=3):
        if self.image:
            try:
                # Konwersja obrazu na skalę szarości
                grayscale_image = ImageOps.grayscale(self.image)

                # Skalowanie obrazu do mniejszego rozmiaru (np. 256x256)
                scaled_image = grayscale_image.resize((512, 512))
                image_np = np.array(scaled_image)

                # Przygotowanie danych dla FCM
                flattened_image = image_np.flatten().astype(np.float64)
                flattened_image /= 255.0  # Normalizacja do zakresu 0-1
                data = np.vstack((flattened_image, np.zeros_like(flattened_image)))

                # Wykonanie Fuzzy C-means
                cntr, u, _, _, _, _, _ = fuzz.cluster.cmeans(
                    data, c=n_clusters, m=2, error=0.005, maxiter=1000, init=None
                )

                # Przypisanie pikseli do klastrów
                cluster_membership = np.argmax(u, axis=0)
                clustered_image = cluster_membership.reshape(image_np.shape)

                # Normalizacja i przywrócenie rozmiaru
                clustered_image = (clustered_image * (255 // (n_clusters - 1))).astype(np.uint8)
                resized_clustered_image = Image.fromarray(clustered_image).resize(self.image.size)

                self.image = resized_clustered_image
                return self.image

            except Exception as e:
                messagebox.showerror("Błąd", f"Rozmyta metoda c-średnich nie powiodła się: {e}")
                return None
        else:
            messagebox.showwarning("Błąd", "Najpierw wczytaj obraz.")
            return None
