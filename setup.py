from setuptools import setup, find_packages

setup(
    name="expense-tracker",
    version="1.0.0",
    author="[Фрицлер Денис Александрович]",
    description="GUI приложение для отслеживания личных расходов",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "expense-tracker=src.main:main",
        ],
    },
)