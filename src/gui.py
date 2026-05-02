# GUI приложения Expense Tracker
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.validator import Validator
from src.data_manager import DataManager
from src.config import CATEGORIES, DATE_FORMAT

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker - Трекер расходов")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        self.data_manager = DataManager()
        self.expenses = self.data_manager.load_expenses()
        
        self.setup_ui()
        self.refresh_table()
        self.update_total_display()
    
    def setup_ui(self):
        # Основная рамка
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === Форма добавления расхода ===
        form_frame = ttk.LabelFrame(main_frame, text="Добавить расход", padding="10")
        form_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Сумма
        ttk.Label(form_frame, text="Сумма (₽):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.amount_entry = ttk.Entry(form_frame, width=20)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Категория
        ttk.Label(form_frame, text="Категория:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=CATEGORIES, width=15)
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)
        self.category_combo.set(CATEGORIES[0])
        
        # Дата
        ttk.Label(form_frame, text=f"Дата ({DATE_FORMAT}):").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.date_entry = ttk.Entry(form_frame, width=15)
        self.date_entry.grid(row=0, column=5, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime(DATE_FORMAT))
        
        # Кнопка добавления
        self.add_btn = ttk.Button(form_frame, text="➕ Добавить расход", command=self.add_expense)
        self.add_btn.grid(row=0, column=6, padx=10, pady=5)
        
        # === Фильтрация ===
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding="10")
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Фильтр по категории
        ttk.Label(filter_frame, text="Фильтр по категории:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.filter_category_var = tk.StringVar(value="Все")
        self.filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_category_var, 
                                          values=["Все"] + CATEGORIES, width=15)
        self.filter_combo.grid(row=0, column=1, padx=5)
        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Фильтр по дате от
        ttk.Label(filter_frame, text="Дата от:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.date_from_entry = ttk.Entry(filter_frame, width=12)
        self.date_from_entry.grid(row=0, column=3, padx=5)
        
        # Фильтр по дате до
        ttk.Label(filter_frame, text="Дата до:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.date_to_entry = ttk.Entry(filter_frame, width=12)
        self.date_to_entry.grid(row=0, column=5, padx=5)
        
        # Кнопка применить фильтр
        self.filter_btn = ttk.Button(filter_frame, text="🔍 Применить фильтр", command=self.apply_filters)
        self.filter_btn.grid(row=0, column=6, padx=10)
        
        # Кнопка сбросить фильтр
        self.reset_filter_btn = ttk.Button(filter_frame, text="🔄 Сбросить", command=self.reset_filters)
        self.reset_filter_btn.grid(row=0, column=7, padx=5)
        
        # === Таблица расходов ===
        table_frame = ttk.LabelFrame(main_frame, text="Список расходов", padding="10")
        table_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Создание Treeview
        columns = ("id", "amount", "category", "date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("amount", text="Сумма (₽)")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")
        
        self.tree.column("id", width=50)
        self.tree.column("amount", width=120)
        self.tree.column("category", width=150)
        self.tree.column("date", width=120)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Кнопка удаления
        self.delete_btn = ttk.Button(table_frame, text="🗑️ Удалить выбранное", command=self.delete_expense)
        self.delete_btn.grid(row=1, column=0, pady=10)
        
        # === Сумма за период ===
        total_frame = ttk.LabelFrame(main_frame, text="Статистика", padding="10")
        total_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.total_label = ttk.Label(total_frame, text="Общая сумма за период: 0.00 ₽", font=("Arial", 12, "bold"))
        self.total_label.pack()
        
        # Кнопки управления
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.save_btn = ttk.Button(control_frame, text="💾 Сохранить в JSON", command=self.save_to_json)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.load_btn = ttk.Button(control_frame, text="📂 Загрузить из JSON", command=self.load_from_json)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(control_frame, text="⚠️ Очистить все", command=self.clear_all)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
    
    def add_expense(self):
        """Добавление расхода с валидацией"""
        amount_str = self.amount_entry.get()
        category = self.category_var.get()
        date_str = self.date_entry.get()
        
        is_valid_amount, amount_or_error = Validator.validate_amount(amount_str)
        if not is_valid_amount:
            messagebox.showerror("Ошибка", amount_or_error)
            return
        
        is_valid_category, category_error = Validator.validate_category(category)
        if not is_valid_category:
            messagebox.showerror("Ошибка", category_error)
            return
        
        is_valid_date, date_error = Validator.validate_date(date_str)
        if not is_valid_date:
            messagebox.showerror("Ошибка", date_error)
            return
        
        amount = amount_or_error
        
        new_id = max([e["id"] for e in self.expenses], default=0) + 1
        new_expense = {
            "id": new_id,
            "amount": amount,
            "category": category,
            "date": date_str
        }
        
        self.expenses.append(new_expense)
        self.data_manager.save_expenses(self.expenses)
        
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime(DATE_FORMAT))
        
        self.refresh_table()
        self.update_total_display()
        messagebox.showinfo("Успех", f"Расход добавлен! ID: {new_id}")
    
    def delete_expense(self):
        """Удаление выбранного расхода"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите запись для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный расход?"):
            for item in selected:
                item_id = int(self.tree.item(item)["values"][0])
                self.expenses = [e for e in self.expenses if e["id"] != item_id]
            
            self.data_manager.save_expenses(self.expenses)
            self.refresh_table()
            self.update_total_display()
            messagebox.showinfo("Успех", "Расход(ы) удалены")
    
    def apply_filters(self):
        """Применение фильтров"""
        self.refresh_table()
        self.update_total_display()
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.filter_category_var.set("Все")
        self.date_from_entry.delete(0, tk.END)
        self.date_to_entry.delete(0, tk.END)
        self.refresh_table()
        self.update_total_display()
    
    def get_filtered_expenses(self):
        """Возвращаем отфильтрованный список расходов"""
        filtered = self.expenses.copy()
        
        # Фильтр по категории
        selected_category = self.filter_category_var.get()
        if selected_category != "Все":
            filtered = [e for e in filtered if e["category"] == selected_category]
        
        # Фильтр по дате от
        date_from = self.date_from_entry.get().strip()
        if date_from:
            try:
                datetime.strptime(date_from, DATE_FORMAT)
                filtered = [e for e in filtered if e["date"] >= date_from]
            except ValueError:
                pass
        
        # Фильтр по дате до
        date_to = self.date_to_entry.get().strip()
        if date_to:
            try:
                datetime.strptime(date_to, DATE_FORMAT)
                filtered = [e for e in filtered if e["date"] <= date_to]
            except ValueError:
                pass
        
        return filtered
    
    def refresh_table(self):
        """Обновление таблицы"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filtered_expenses = self.get_filtered_expenses()
        
        for expense in filtered_expenses:
            self.tree.insert("", tk.END, values=(
                expense["id"],
                f"{expense['amount']:.2f}",
                expense["category"],
                expense["date"]
            ))
    
    def update_total_display(self):
        """Обновление отображения суммы за период"""
        filtered = self.get_filtered_expenses()
        total = sum(e["amount"] for e in filtered)
        self.total_label.config(text=f"📊 Общая сумма за период: {total:.2f} ₽")
    
    def save_to_json(self):
        """Сохранение в JSON"""
        if self.data_manager.save_expenses(self.expenses):
            messagebox.showinfo("Успех", "Данные сохранены в JSON файл")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные")
    
    def load_from_json(self):
        """Загрузка из JSON"""
        loaded = self.data_manager.load_expenses()
        if loaded is not None:
            self.expenses = loaded
            self.refresh_table()
            self.update_total_display()
            messagebox.showinfo("Успех", f"Загружено {len(self.expenses)} записей")
        else:
            messagebox.showerror("Ошибка", "Не удалось загрузить данные")
    
    def clear_all(self):
        """Очистка всех данных"""
        if messagebox.askyesno("Внимание!", "Все данные будут удалены безвозвратно. Продолжить?"):
            self.expenses = []
            self.data_manager.clear_data()
            self.refresh_table()
            self.update_total_display()
            messagebox.showinfo("Успех", "Все данные очищены")