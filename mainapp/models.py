from django.db import models

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Имя')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(verbose_name='активна', default=True)

    class Meta:
        verbose_name = 'катгория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True, verbose_name='Имя')
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).\
            order_by('category', 'name')

    def __str__(self):
        return f'{self.name} {self.category.name}'
