# Работа с JSON
import json
import os
from src.config import DATA_FILE

class DataManager:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
    
    def save_expenses(self, expenses: list) -> bool:
        """Сохраняем список расходов в JSON файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(expenses, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False
    
    def load_expenses(self) -> list:
        """Загружаем список расходов из JSON файла"""
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                expenses = json.load(f)
                return expenses if isinstance(expenses, list) else []
        except (json.JSONDecodeError, Exception) as e:
            print(f"Ошибка загрузки: {e}")
            return []
    
    def clear_data(self) -> bool:
        """Очищаем файл данных"""
        return self.save_expenses([])