from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Table {self.number} ({self.capacity} seats)"


class Reservation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('table', 'date', 'time')

    def clean(self):
        if self.guests > self.table.capacity:
            raise ValidationError(
                f"Table {self.table.number} can only accommodate "
                f"{self.table.capacity} guests."
            )

    def __str__(self):
        return (
            f"Reservation for {self.name} at "
            f"Table {self.table.number} on {self.date} at {self.time}"
        )
