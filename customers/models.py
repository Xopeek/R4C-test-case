from django.db import models


class Customer(models.Model):
    """Заказчик."""
    email = models.CharField(
        'Заказчик',
        max_length=255,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        return self.email
