import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from colorthief import ColorThief

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos de Imagen", "*.jpg;*.jpeg;*.png")])
    
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)

        label_image.config(image=photo)
        label_image.image = photo

        label_result.config(text="Procesando...")

        root.update()

        color_hex = get_dominant_color(file_path)

        label_result.config(text=f"Color Predominante: {color_hex}")
        label_color.config(bg=color_hex)


def get_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=10)
    return '#%02x%02x%02x' % dominant_color

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


