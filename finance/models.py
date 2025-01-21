from django.db import models



class Revenue(models.Model):
    date = models.DateField(unique=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Выручка за {self.date}: {self.total_revenue}"
