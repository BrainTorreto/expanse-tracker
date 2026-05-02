# Модуль валидации ввода
from datetime import datetime
from src.config import DATE_FORMAT

class Validator:
    @staticmethod
    def validate_amount(amount_str: str) -> tuple[bool, str | float]:
        """Проверяем сумму: положительное число"""
        if not amount_str or amount_str.strip() == "":
            return False, "Сумма не может быть пустой"
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                return False, "Сумма должна быть положительным числом"
            if amount > 1_000_000:
                return False, "Сумма не может превышать 1 000 000"
            return True, amount
        except ValueError:
            return False, "Введите корректное число"
    
    @staticmethod
    def validate_date(date_str: str) -> tuple[bool, str | None]:
        """Проверяем дату в формате ГГГГ-ММ-ДД"""
        if not date_str or date_str.strip() == "":
            return False, "Дата не может быть пустой"
        
        try:
            datetime.strptime(date_str, DATE_FORMAT)
            return True, None
        except ValueError:
            return False, f"Неверный формат даты. Используйте {DATE_FORMAT}"
    
    @staticmethod
    def validate_category(category: str) -> tuple[bool, str | None]:
        """Проверяем, что категория выбрана"""
        if not category or category == "":
            return False, "Выберите категорию"
        return True, None