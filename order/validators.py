from django.core.exceptions import ValidationError
from typing import Any, Tuple, Dict


class ValidatePrice:
    """
    Валидатор для проверки, что цена не меньше минимального значения.
    """

    def __init__(self, min_price: float = 0) -> None:
        """
        Инициализация валидатора.
        :param min_price: Минимально допустимая цена (по умолчанию 0).
        """
        self.min_price = min_price

    def __call__(self, value: float) -> None:
        """
        Проверка значения.
        :param value: Проверяемое значение цены.
        :raises ValidationError: Если цена меньше минимального значения.
        """
        if value < self.min_price:
            raise ValidationError(f"Цена не может быть меньше {self.min_price} руб.")

    def deconstruct(self) -> Tuple[str, list, Dict[str, Any]]:
        """
        Метод для поддержки миграций.
        :return: Кортеж с информацией для сериализации валидатора.
        """
        return (
            "order.validators.ValidatePrice",  # Путь к классу
            [],  # Аргументы для __init__
            {"min_price": self.min_price},
        )
