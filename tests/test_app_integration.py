import unittest
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_manager import DataManager
from src.validator import Validator
from src.config import CATEGORIES

class TestAppIntegration(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "test_integration.json"
        self.dm = DataManager(self.test_file)
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    # === Интеграционные тесты ===
    def test_add_and_save_expense_flow(self):
        """Тест полного цикла: валидация -> добавление -> сохранение -> загрузка"""
        # Валидация
        is_valid, amount = Validator.validate_amount("150.50")
        self.assertTrue(is_valid)
        
        is_valid_date, _ = Validator.validate_date("2024-05-20")
        self.assertTrue(is_valid_date)
        
        # Создание расхода
        expense = {"id": 1, "amount": amount, "category": "Еда", "date": "2024-05-20"}
        
        # Сохранение
        self.dm.save_expenses([expense])
        
        # Загрузка и проверка
        loaded = self.dm.load_expenses()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["amount"], 150.50)
    
    def test_filtering_workflow(self):
        """Тест работы фильтрации с данными"""
        expenses = [
            {"id": 1, "amount": 100, "category": "Еда", "date": "2024-05-01"},
            {"id": 2, "amount": 200, "category": "Транспорт", "date": "2024-05-02"},
            {"id": 3, "amount": 150, "category": "Еда", "date": "2024-05-03"}
        ]
        
        self.dm.save_expenses(expenses)
        loaded = self.dm.load_expenses()
        
        # Фильтр по категории "Еда"
        filtered = [e for e in loaded if e["category"] == "Еда"]
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]["amount"], 100)
        
        # Фильтр по дате
        filtered_by_date = [e for e in loaded if e["date"] >= "2024-05-02"]
        self.assertEqual(len(filtered_by_date), 2)
    
    def test_total_sum_calculation(self):
        """Тест подсчёта суммы"""
        expenses = [
            {"id": 1, "amount": 100.50, "category": "Еда", "date": "2024-05-01"},
            {"id": 2, "amount": 200.25, "category": "Транспорт", "date": "2024-05-02"},
            {"id": 3, "amount": 50.00, "category": "Еда", "date": "2024-05-03"}
        ]
        
        total = sum(e["amount"] for e in expenses)
        self.assertEqual(total, 350.75)
    
    def test_edge_case_empty_database(self):
        """Граничный случай: пустая база"""
        self.dm.clear_data()
        loaded = self.dm.load_expenses()
        self.assertEqual(loaded, [])
        
        total = sum(e["amount"] for e in loaded)
        self.assertEqual(total, 0)

if __name__ == '__main__':
    unittest.main()