import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import KMeans
import requests

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos de Imagen", "*.jpg;*.jpeg;*.png")])
    
    if file_path:
        try:
            image = Image.open(file_path)
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)

            label_image.config(image=photo)
            label_image.image = photo

            label_result.config(text="Procesando...")

            root.update()

            root.after(100, process_image, file_path)

        except Exception as e:
            label_result.config(text=f"Error al cargar la imagen: {e}")

def process_image(file_path):
    color_hex = get_dominant_color(file_path)

    color_name = get_color_name(color_hex)

    label_result.config(text=f"Color Predominante: {color_hex} ({color_name})")
    label_color.config(bg=color_hex)

def get_dominant_color(image_path):
    try:
        image = Image.open(image_path)
        image = image.convert("RGB")
        
        image = image.resize((200, 200))
        pixels = np.array(image).reshape(-1, 3)
        
        kmeans = KMeans(n_clusters=5, n_init=10).fit(pixels)

        labels = kmeans.labels_

        unique, counts = np.unique(labels, return_counts=True)
        cluster_sizes = dict(zip(unique, counts))

        sorted_centroids = sorted(zip(kmeans.cluster_centers_, unique), key=lambda x: cluster_sizes[x[1]], reverse=True)
        dominant_color = sorted_centroids[0][0]

        color_hex = '#{:02x}{:02x}{:02x}'.format(int(dominant_color[0]), int(dominant_color[1]), int(dominant_color[2]))

        return color_hex

    except Exception as e:
        return f"Error: {e}"

def get_color_name(hex_code):

    url = "https://www.thecolorapi.com/id"
    params = {'hex': hex_code.lstrip('#')}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            color_data = response.json()
            return color_data['name']['value']
        else:
            return "Desconocido"
    except Exception as e:
        return "Error en la API"

root = tk.Tk()
root.title("Análisis de Color Predominante")
root.geometry("600x500")

btn_open_image = tk.Button(root, text="Seleccionar Imagen", command=open_image)
btn_open_image.pack(pady=10)

label_image = tk.Label(root)
label_image.pack()

label_result = tk.Label(root, text="Color Predominante: ", font=("Arial", 12))
label_result.pack(pady=10)

label_color = tk.Label(root, text="     ", width=20, height=2, font=("Arial", 12))
label_color.pack()

label_original_image = tk.Label(root)
label_original_image.place_forget()

root.mainloop()
