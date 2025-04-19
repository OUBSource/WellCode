import tkinter as tk
from tkinter import messagebox, filedialog
import zipfile
import os
import shutil
import subprocess
import sys

# Класс для вывода текста в текстовое поле
class OutputRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        if message != '\n':
            self.text_widget.insert(tk.END, message)
            self.text_widget.yview(tk.END)

    def flush(self):
        pass

# GUI
def create_gui():
    root = tk.Tk()
    root.title("Проектный GUI")

    code_text = tk.Text(root, width=60, height=20)
    code_text.pack(pady=10)
    
    def build_code():
        code = code_text.get("1.0", tk.END)
        if not code.strip():
            messagebox.showerror("Ошибка", "Нет кода для сборки!")
            return
        
        create_project_structure()

        with open("project/main.py", "w", encoding="utf-8") as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write(code)

        create_bra_file()

        # Удаляем временную папку project
        shutil.rmtree("project", ignore_errors=True)

        messagebox.showinfo("Успех", "Проект успешно собран в .bra файл!")

    def choose_bra_file():
        file_path = filedialog.askopenfilename(filetypes=[("BRA files", "*.bra")])
        if file_path:
            open_output_window(file_path)

    def open_output_window(file_path):
        output_window = tk.Toplevel(root)
        output_window.title("Вывод скрипта")

        output_text = tk.Text(output_window, width=80, height=20)
        output_text.pack(pady=10)

        sys.stdout = OutputRedirector(output_text)

        try:
            with zipfile.ZipFile(file_path, 'r') as zipf:
                zipf.extractall("project")

            subprocess.run(["python", "project/main.py"], check=True)
            messagebox.showinfo("Успех", ".bra файл успешно выполнен!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Ошибка", "Не удалось запустить .bra файл.")
        except zipfile.BadZipFile:
            messagebox.showerror("Ошибка", "Выбранный файл не является корректным архивом.")
        finally:
            sys.stdout = sys.__stdout__

    tk.Button(root, text="Билд", command=build_code).pack(pady=10)
    tk.Button(root, text="Выбрать и запустить .bra", command=choose_bra_file).pack(pady=10)

    root.mainloop()

def create_project_structure():
    os.makedirs("project/libs", exist_ok=True)
    os.makedirs("project/manifest", exist_ok=True)

    with open("project/libs/projectlib.dll", "w", encoding="utf-8") as f:
        f.write("Это тестовая библиотека projectlib.dll.")

    with open("project/manifest/project.tra", "w", encoding="utf-8") as f:
        f.write("Это манифест для проекта.")

def create_bra_file():
    with zipfile.ZipFile("project.bra", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root_dir, dirs, files in os.walk("project"):
            for file in files:
                file_path = os.path.join(root_dir, file)
                zipf.write(file_path, os.path.relpath(file_path, "project"))

def main():
    create_gui()

if __name__ == "__main__":
    main()
