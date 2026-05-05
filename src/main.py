import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary - Дневник погоды")
        self.root.geometry("800x600")
        
        self.entries = []
        self.filtered_entries = []
        self.filename = "weather_diary.json"
        
        self.load_data()
        self.create_widgets()
        self.update_table()
    
    def create_widgets(self):
        # Рамка для ввода
        input_frame = ttk.LabelFrame(self.root, text="Добавить запись", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Дата
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="w", padx=5)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Температура
        ttk.Label(input_frame, text="Температура (°C):").grid(row=0, column=2, sticky="w", padx=5)
        self.temp_entry = ttk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=3, padx=5)
        
        # Описание
        ttk.Label(input_frame, text="Описание:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.desc_entry = ttk.Entry(input_frame, width=50)
        self.desc_entry.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        
        # Осадки
        self.precip_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Осадки", variable=self.precip_var).grid(row=2, column=0, padx=5, pady=5)
        
        # Кнопка добавления
        ttk.Button(input_frame, text="➕ Добавить запись", command=self.add_entry).grid(row=2, column=3, sticky="e", padx=5)
        
        # Рамка для фильтров
        filter_frame = ttk.LabelFrame(self.root, text="Фильтры", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=0, padx=5)
        self.filter_date = ttk.Entry(filter_frame, width=15)
        self.filter_date.grid(row=0, column=1, padx=5)
        
        ttk.Label(filter_frame, text="Фильтр по температуре (>):").grid(row=0, column=2, padx=5)
        self.filter_temp = ttk.Entry(filter_frame, width=10)
        self.filter_temp.grid(row=0, column=3, padx=5)
        
        ttk.Button(filter_frame, text="🔍 Применить фильтр", command=self.apply_filter).grid(row=0, column=4, padx=5)
        ttk.Button(filter_frame, text="🔄 Сбросить фильтр", command=self.reset_filter).grid(row=0, column=5, padx=5)
        
        # Таблица для отображения
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("date", "temperature", "description", "precipitation")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        
        self.tree.heading("date", text="Дата")
        self.tree.heading("temperature", text="Температура (°C)")
        self.tree.heading("description", text="Описание")
        self.tree.heading("precipitation", text="Осадки")
        
        self.tree.column("date", width=100)
        self.tree.column("temperature", width=100)
        self.tree.column("description", width=400)
        self.tree.column("precipitation", width=80)
        
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Кнопки управления
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(control_frame, text="💾 Сохранить в JSON", command=self.save_to_json).pack(side="left", padx=5)
        ttk.Button(control_frame, text="📂 Загрузить из JSON", command=self.load_from_json).pack(side="left", padx=5)
        ttk.Button(control_frame, text="🗑 Удалить выбранное", command=self.delete_entry).pack(side="left", padx=5)
        
        self.status_label = ttk.Label(self.root, text=f"Всего записей: {len(self.entries)}", relief="sunken")
        self.status_label.pack(fill="x", padx=10, pady=5)
    
    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def add_entry(self):
        date = self.date_entry.get()
        temp = self.temp_entry.get()
        description = self.desc_entry.get()
        precipitation = self.precip_var.get()
        
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return
        
        try:
            temp_float = float(temp)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return
        
        if not description.strip():
            messagebox.showerror("Ошибка", "Описание не может быть пустым!")
            return
        
        entry = {
            "date": date,
            "temperature": temp_float,
            "description": description,
            "precipitation": "Да" if precipitation else "Нет"
        }
        
        self.entries.append(entry)
        self.entries.sort(key=lambda x: x["date"])
        
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)
        
        self.update_table()
        self.save_to_json()
        messagebox.showinfo("Успех", "Запись добавлена!")
    
    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        display_entries = self.filtered_entries if self.filtered_entries else self.entries
        
        for entry in display_entries:
            self.tree.insert("", "end", values=(
                entry["date"],
                entry["temperature"],
                entry["description"],
                entry["precipitation"]
            ))
        
        self.status_label.config(text=f"Всего записей: {len(self.entries)} | Отображено: {len(display_entries)}")
    
    def apply_filter(self):
        filter_date = self.filter_date.get()
        filter_temp_str = self.filter_temp.get()
        
        self.filtered_entries = self.entries.copy()
        
        if filter_date:
            if not self.validate_date(filter_date):
                messagebox.showerror("Ошибка", "Неверный формат даты в фильтре!")
                return
            self.filtered_entries = [e for e in self.filtered_entries if e["date"] == filter_date]
        
        if filter_temp_str:
            try:
                filter_temp = float(filter_temp_str)
                self.filtered_entries = [e for e in self.filtered_entries if e["temperature"] > filter_temp]
            except ValueError:
                messagebox.showerror("Ошибка", "Температура фильтра должна быть числом!")
                return
        
        self.update_table()
    
    def reset_filter(self):
        self.filter_date.delete(0, tk.END)
        self.filter_temp.delete(0, tk.END)
        self.filtered_entries = []
        self.update_table()
    
    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите запись для удаления!")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранную запись?"):
            values = self.tree.item(selected[0])["values"]
            
            for i, entry in enumerate(self.entries):
                if (entry["date"] == values[0] and 
                    entry["temperature"] == values[1] and 
                    entry["description"] == values[2]):
                    del self.entries[i]
                    break
            
            self.reset_filter()
            self.save_to_json()
            messagebox.showinfo("Успех", "Запись удалена!")
    
    def save_to_json(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=2)
            self.status_label.config(text=f"Сохранено в {self.filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
    
    def load_from_json(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.entries = json.load(f)
                self.reset_filter()
                self.status_label.config(text=f"Загружено из {self.filename}")
                messagebox.showinfo("Успех", f"Загружено {len(self.entries)} записей!")
            else:
                messagebox.showwarning("Внимание", f"Файл {self.filename} не найден!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")
    
    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.entries = json.load(f)
            except:
                self.entries = []

def main():
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()

if __name__ == "__main__":
    main()