from django.db import models

# Create your models here.


class Item(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=64, verbose_name='Название')
    description = models.TextField(max_length=512, verbose_name='Описание',
                                   blank=True)
    price = models.IntegerField(default=0, verbose_name='Стоимость')

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
