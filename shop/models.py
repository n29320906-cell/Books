from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Жанр")

    def _str_(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Аталышы")
    author = models.CharField(max_length=100, verbose_name="Автору")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Баасы"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Сүрөттөмөсү"
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="Жанры"
    )
    image = models.ImageField(
        upload_to="book_covers/",
        blank=True,
        null=True,
        verbose_name="Сүрөтү"
    )

    def _str_(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")

    def _str_(self):
        return f"{self.user.username} - {self.book.title}"


class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.book.price * self.quantity

    def _str_(self):
        return f"{self.user.username} - {self.book.title} x {self.quantity}"