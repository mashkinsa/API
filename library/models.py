from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    biography = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='authors/photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)],
        help_text="Год выпуска должен быть от 1000 до 9999"
    )
    genre = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='books/covers/', blank=True, null=True)
    book_file = models.FileField(upload_to='books/files/', blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author', 'publication_year', 'publisher'],
                name='unique_book_constraint'
            )
        ]

    def __str__(self):
        return self.title
