import tkinter as tk

window = tk.Tk()
window.title("Цвета радуги")
window.geometry("200x500")


color_name_label = tk.Label(window, text="", font=("Arial", 14))
color_name_label.pack(pady=5)



color_code_entry = tk.Entry(
    window,
    width=20,
    font=("Arial", 12),
    justify='center'
)
color_code_entry.pack(pady=5)


buttons_frame = tk.Frame(window)
buttons_frame.pack(pady=1)

colors = [
    ("Красный", "#ff0000"),
    ("Оранжевый", "#ff7400"),
    ("Желтый", "#ffff00"),
    ("Зеленый", "#00ff00"),
    ("Голубой", "#007dff"),
    ("Синий", "#0000ff"),
    ("Фиолетовый", "#7d00ff")
]

def show_color_info(color_name, color_code):
    color_code_entry.config(state='normal')
    color_code_entry.delete(0, tk.END)
    color_code_entry.insert(0, color_code)
    color_code_entry.config(state='readonly')


for color_name, color_code in colors:
    button = tk.Button(
        buttons_frame,
        bg=color_code,
        fg="black" if color_name == "Желтый" else "white",
        width=20,
        height=2,
        command=lambda name=color_name, code=color_code: show_color_info(name, code)
    )
    button.pack(pady=1)

window.mainloop()