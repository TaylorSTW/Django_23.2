from django.conf import settings
from django.db import models


NULLABLE = {
    'null': True,
    'blank': True,
}

class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Category')
    description = models.TextField(verbose_name='Description')
    # created_at = models.DateTimeField(**NULLABLE, verbose_name='Created At')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):

    name = models.CharField(max_length=250, verbose_name='Name')
    description = models.TextField(**NULLABLE, verbose_name='Description')
    photo = models.ImageField(upload_to='shop/',**NULLABLE, verbose_name='Photo')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    price = models.IntegerField(verbose_name='Price')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')
    date_modified = models.DateTimeField(**NULLABLE, verbose_name='Date Modified')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Owner')

    def __str__(self):
        return f'{self.name} (Price: {self.price}): {self.description}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Contact(models.Model):
    name = models.CharField(max_length=250, verbose_name='Contact name')
    email = models.EmailField(max_length=250, verbose_name='Email')
    message = models.TextField(**NULLABLE, verbose_name='Message')

    def __str__(self):
        return f'{self.name} ({self.email}): {self.message}'

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Title')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    content = models.TextField(verbose_name='Content')
    preview = models.ImageField(upload_to='blog/',**NULLABLE, verbose_name='Preview')
    date_created = models.DateTimeField(verbose_name='Date Created')
    is_published = models.BooleanField(default=True, verbose_name='published')
    views_count = models.IntegerField(default=0, verbose_name='views')

    def __str__(self):
        return f"{self.title} ({self.date_created.date()}): {self.content}"

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    number = models.IntegerField(verbose_name='Version number')
    name = models.CharField(max_length=100, verbose_name='Version name')
    is_active = models.BooleanField(default=True, verbose_name='Active')

    def __str__(self):
        return f'Версия №{self.number}: {self.name}'

    class Meta:
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'