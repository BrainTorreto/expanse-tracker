import tkinter as tk
import sys
import os

# Добавляем текущую папку в путь
sys.path.insert(0, os.getcwd())

# Импорт
from src.gui import ExpenseTracker

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
