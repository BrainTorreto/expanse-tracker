import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.validator import Validator

class TestValidator(unittest.TestCase):
    
    # === Позитивные тесты ===
    def test_valid_amount_positive(self):
        is_valid, result = Validator.validate_amount("100")
        self.assertTrue(is_valid)
        self.assertEqual(result, 100.0)
    
    def test_valid_amount_decimal(self):
        is_valid, result = Validator.validate_amount("99.99")
        self.assertTrue(is_valid)
        self.assertEqual(result, 99.99)
    
    def test_valid_date_correct_format(self):
        is_valid, error = Validator.validate_date("2024-05-15")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_valid_category_selected(self):
        is_valid, error = Validator.validate_category("Еда")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    # === Негативные тесты ===
    def test_invalid_amount_negative(self):
        is_valid, error = Validator.validate_amount("-50")
        self.assertFalse(is_valid)
        self.assertEqual(error, "Сумма должна быть положительным числом")
    
    def test_invalid_amount_zero(self):
        is_valid, error = Validator.validate_amount("0")
        self.assertFalse(is_valid)
        self.assertEqual(error, "Сумма должна быть положительным числом")
    
    def test_invalid_amount_text(self):
        is_valid, error = Validator.validate_amount("abc")
        self.assertFalse(is_valid)
        self.assertEqual(error, "Введите корректное число")
    
    def test_invalid_amount_empty(self):
        is_valid, error = Validator.validate_amount("")
        self.assertFalse(is_valid)
        self.assertEqual(error, "Сумма не может быть пустой")
    
    def test_invalid_date_wrong_format(self):
        is_valid, error = Validator.validate_date("15-05-2024")
        self.assertFalse(is_valid)
        self.assertTrue("Неверный формат даты" in error)
    
    def test_invalid_date_empty(self):
        is_valid, error = Validator.validate_date("")
        self.assertFalse(is_valid)
        self.assertEqual(error, "Дата не может быть пустой")
    
    def test_invalid_category_empty(self):
        is_valid, error = Validator.validate_category("")
        self.assertFalse(is_valid)
        self.assertEqual(error, "Выберите категорию")
    
    # === Граничные тесты ===
    def test_boundary_amount_very_large(self):
        is_valid, error = Validator.validate_amount("1000001")
        self.assertFalse(is_valid)
        self.assertEqual(error, "Сумма не может превышать 1 000 000")
    
    def test_boundary_amount_max_valid(self):
        is_valid, result = Validator.validate_amount("1000000")
        self.assertTrue(is_valid)
        self.assertEqual(result, 1000000.0)
    
    def test_boundary_amount_min_valid(self):
        is_valid, result = Validator.validate_amount("0.01")
        self.assertTrue(is_valid)
        self.assertEqual(result, 0.01)
    
    def test_boundary_date_leap_year(self):
        is_valid, error = Validator.validate_date("2024-02-29")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_boundary_date_last_day(self):
        is_valid, error = Validator.validate_date("2024-12-31")
        self.assertTrue(is_valid)
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()