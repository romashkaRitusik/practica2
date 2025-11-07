import tkinter as tk
from tkinter import messagebox

def register():
    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()

    if not username or not password or not confirm_password:
        label_error.config(text="Все поля должны быть заполнены.", fg="red")
        return

    if password != confirm_password:
        label_error.config(text="Пароли не совпадают.", fg="red")
        return

    label_error.config(text="Регистрация успешна!", fg="green")
    messagebox.showinfo("Успех", f"Пользователь {username} успешно зарегистрирован!")

    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_confirm_password.delete(0, tk.END)

root = tk.Tk()
root.title("Форма регистрации")
root.geometry("300x300")
root.resizable(False, False)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

tk.Label(main_frame, text="Имя пользователя:").grid(row=0, column=0, sticky="w", pady=5)
entry_username = tk.Entry(main_frame, width=30)
entry_username.grid(row=1, column=0, columnspan=2, pady=5)

tk.Label(main_frame, text="Пароль:").grid(row=2, column=0, sticky="w", pady=5)
entry_password = tk.Entry(main_frame, show="*", width=30)
entry_password.grid(row=3, column=0, columnspan=2, pady=5)

tk.Label(main_frame, text="Подтверждение пароля:").grid(row=4, column=0, sticky="w", pady=5)
entry_confirm_password = tk.Entry(main_frame, show="*", width=30)
entry_confirm_password.grid(row=5, column=0, columnspan=2, pady=5)

btn_register = tk.Button(main_frame, text="Зарегистрироваться", command=register, width=20)
btn_register.grid(row=6, column=0, columnspan=2, pady=15)

label_error = tk.Label(main_frame, text="")
label_error.grid(row=7, column=0, columnspan=2, pady=5)

root.mainloop()