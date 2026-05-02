# Точка входа в приложение
import tkinter as tk
from src.gui import ExpenseTracker

def main():
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()