from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.name', read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )

    def validate(self, data):
        title = data.get('title')
        category = data.get('category')
        publisher = data.get('publisher')
        publication_year = data.get('publication_year')

        if category.lower() == 'учебник':
            if Book.objects.filter(
                    title=title,
                    category=category,
                    publisher=publisher,
                    publication_year=publication_year
            ).exists():
                raise serializers.ValidationError(
                    "Учебник с таким названием, издательством и годом издания уже существует"
                )

        elif category.lower() == 'художественное произведение':
            if Book.objects.filter(
                    title=title,
                    category=category,
                    publisher=publisher
            ).exists():
                raise serializers.ValidationError(
                    "Художественное произведение от этого издательства уже существует"
                )

        return data

    class Meta:
        model = Book
        fields = '__all__'
