from django.core.exceptions import ValidationError


class ValidatePrice:
    def __init__(self,min_price=0):
        self.min_price = min_price

    def __call__(self, value):
        if value < self.min_price:
            raise ValidationError(f"Цена не может быть меньше - {self.min_price}")

    def deconstruct(self):
        return (
            "orders.validators.ValidatePrice",
            [],
            {},
        )
