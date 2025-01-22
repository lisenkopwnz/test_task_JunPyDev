from django.db import models


class Revenue(models.Model):
    """
        Модель для хранения данных о выручке за определённый день.

        Эта модель используется для учёта ежедневной выручки. Каждая запись содержит
        дату и общую сумму выручки за этот день. Дата должна быть уникальной, чтобы
        избежать дублирования записей.

        Атрибуты:
            date (DateField): Дата, за которую учитывается выручка. Уникальное поле.
            total_revenue (DecimalField): Общая сумма выручки за день. Максимум 10 цифр,
                                         из которых 2 после запятой.

        Методы:
            __str__(): Возвращает строковое представление записи в формате:
                       "Выручка за <дата>: <сумма>".
    """
    date = models.DateField(unique=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Выручка"
        verbose_name_plural = "Выручка"
        ordering = ['-date']

    def __str__(self):
        """ Возвращает строковое представление записи."""
        return f"Выручка за {self.date}: {self.total_revenue:.2f}"
