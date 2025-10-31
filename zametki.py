import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime


class NotesEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор заметок")
        self.root.geometry("800x600")

        # Данные для хранения заметок
        self.notes = []
        self.current_note_index = None
        self.filtered_notes = []

        self.create_widgets()
        self.load_notes()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(main_frame, text="Редактор заметок", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        ttk.Label(left_frame, text="Поиск заметок:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_search = ttk.Entry(left_frame, width=25)
        self.entry_search.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        self.entry_search.bind('<KeyRelease>', self.search_notes)

        self.btn_search = ttk.Button(left_frame, text="Найти", command=self.search_notes)
        self.btn_search.grid(row=1, column=1, padx=5)

        ttk.Label(left_frame, text="Список заметок:").grid(row=2, column=0, sticky=tk.W, pady=5)

        list_frame = ttk.Frame(left_frame)
        list_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.listbox_notes = tk.Listbox(list_frame, width=30, height=20)
        self.listbox_notes.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar_notes = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox_notes.yview)
        scrollbar_notes.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.listbox_notes.configure(yscrollcommand=scrollbar_notes.set)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        self.btn_new = ttk.Button(btn_frame, text="Новая заметка", command=self.new_note)
        self.btn_new.grid(row=0, column=0, padx=2)

        self.btn_delete = ttk.Button(btn_frame, text="Удалить", command=self.delete_note)
        self.btn_delete.grid(row=0, column=1, padx=2)

        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        ttk.Label(right_frame, text="Заголовок:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_title = ttk.Entry(right_frame, width=40)
        self.entry_title.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(right_frame, text="Текст заметки:").grid(row=2, column=0, sticky=tk.W, pady=5)

        text_frame = ttk.Frame(right_frame)
        text_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.text_note = tk.Text(text_frame, width=50, height=25, wrap=tk.WORD)
        self.text_note.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar_text = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_note.yview)
        scrollbar_text.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.text_note.configure(yscrollcommand=scrollbar_text.set)

        save_frame = ttk.Frame(right_frame)
        save_frame.grid(row=4, column=0, pady=10)

        self.btn_save = ttk.Button(save_frame, text="Сохранить заметку", command=self.save_note)
        self.btn_save.grid(row=0, column=0, padx=5)

        self.label_status = ttk.Label(main_frame, text="Всего заметок: 0")
        self.label_status.grid(row=2, column=0, columnspan=2, pady=10)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(3, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(3, weight=1)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.listbox_notes.bind('<<ListboxSelect>>', self.on_note_select)

    def new_note(self):
        """Создание новой заметки"""
        self.current_note_index = None
        self.entry_title.delete(0, tk.END)
        self.text_note.delete(1.0, tk.END)
        self.entry_title.focus()

    def save_note(self):
        """Сохранение заметки"""
        title = self.entry_title.get().strip()
        content = self.text_note.get(1.0, tk.END).strip()

        if not title:
            messagebox.showerror("Ошибка", "Введите заголовок заметки")
            return

        if not content:
            messagebox.showerror("Ошибка", "Введите текст заметки")
            return

        note_data = {
            "title": title,
            "content": content,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if self.current_note_index is None else self.notes[
                self.current_note_index].get("created", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if self.current_note_index is None:
            self.notes.append(note_data)
        else:
            self.notes[self.current_note_index] = note_data

        self.update_notes_list()
        self.save_notes()
        messagebox.showinfo("Успех", "Заметка сохранена")

    def delete_note(self):
        """Удаление выбранной заметки"""
        selected = self.listbox_notes.curselection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заметку для удаления")
            return

        index = selected[0]
        if messagebox.askyesno("Подтверждение", "Удалить выбранную заметку?"):
            if self.filtered_notes:
                note_title = self.filtered_notes[index]
                for i, note in enumerate(self.notes):
                    if note["title"] == note_title:
                        self.notes.pop(i)
                        break
            else:
                self.notes.pop(index)

            self.update_notes_list()
            self.save_notes()
            self.new_note()

    def on_note_select(self, event):
        selected = self.listbox_notes.curselection()
        if selected:
            index = selected[0]

            notes_list = self.filtered_notes if self.filtered_notes else [note["title"] for note in self.notes]

            if index < len(notes_list):
                note_title = notes_list[index]

                for i, note in enumerate(self.notes):
                    if note["title"] == note_title:
                        self.current_note_index = i
                        self.entry_title.delete(0, tk.END)
                        self.entry_title.insert(0, note["title"])
                        self.text_note.delete(1.0, tk.END)
                        self.text_note.insert(1.0, note["content"])
                        break

    def search_notes(self, event=None):
        """Поиск заметок по заголовку и содержимому"""
        search_term = self.entry_search.get().strip().lower()

        if not search_term:
            self.filtered_notes = []
            self.update_notes_list()
            return

        self.filtered_notes = [
            note["title"] for note in self.notes
            if search_term in note["title"].lower() or search_term in note["content"].lower()
        ]

        self.update_notes_list()

    def update_notes_list(self):
        """Обновление списка заметок"""
        self.listbox_notes.delete(0, tk.END)

        notes_list = self.filtered_notes if self.filtered_notes else [note["title"] for note in self.notes]

        for title in notes_list:
            self.listbox_notes.insert(tk.END, title)

        self.label_status.config(text=f"Всего заметок: {len(self.notes)}" +
                                      (f" (найдено: {len(self.filtered_notes)})" if self.filtered_notes else ""))

    def save_notes(self):
        """Сохранение заметок в файл"""
        try:
            with open("notes.json", "w", encoding="utf-8") as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения заметок: {e}")

    def load_notes(self):
        """Загрузка заметок из файла"""
        try:
            if os.path.exists("notes.json"):
                with open("notes.json", "r", encoding="utf-8") as f:
                    self.notes = json.load(f)
                self.update_notes_list()
        except Exception as e:
            print(f"Ошибка загрузки заметок: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesEditor(root)
    root.mainloop()