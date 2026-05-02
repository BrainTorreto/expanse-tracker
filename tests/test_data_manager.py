import unittest
import os
import json
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_manager import DataManager

class TestDataManager(unittest.TestCase):
    
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.test_filename = "test_data.json"
        self.dm = DataManager(self.test_filename)
        self.sample_expenses = [
            {"id": 1, "amount": 100.0, "category": "Еда", "date": "2024-05-15"},
            {"id": 2, "amount": 200.0, "category": "Транспорт", "date": "2024-05-16"}
        ]
    
    def tearDown(self):
        """Очистка после каждого теста"""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    # === Позитивные тесты ===
    def test_save_expenses_success(self):
        result = self.dm.save_expenses(self.sample_expenses)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_filename))
        
        with open(self.test_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(data, self.sample_expenses)
    
    def test_load_expenses_success(self):
        self.dm.save_expenses(self.sample_expenses)
        loaded = self.dm.load_expenses()
        self.assertEqual(loaded, self.sample_expenses)
    
    def test_load_empty_file(self):
        loaded = self.dm.load_expenses()
        self.assertEqual(loaded, [])
    
    def test_clear_data(self):
        self.dm.save_expenses(self.sample_expenses)
        self.dm.clear_data()
        loaded = self.dm.load_expenses()
        self.assertEqual(loaded, [])
    
    # === Негативные тесты ===
    def test_load_corrupted_json(self):
        with open(self.test_filename, 'w') as f:
            f.write("{corrupted json")
        loaded = self.dm.load_expenses()
        self.assertEqual(loaded, [])
    
    def test_save_invalid_data(self):
        result = self.dm.save_expenses(None)
        self.assertFalse(result)
    
    # === Граничные тесты ===
    def test_save_empty_list(self):
        result = self.dm.save_expenses([])
        self.assertTrue(result)
        loaded = self.dm.load_expenses()
        self.assertEqual(loaded, [])
    
    def test_load_nonexistent_file(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
        loaded = self.dm.load_expenses()
        self.assertEqual(loaded, [])

if __name__ == '__main__':
    unittest.main()