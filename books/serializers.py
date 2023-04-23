from rest_framework import serializers
from books.models import Book, Borrowing


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_fee"
        ]


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book"
        ]

    def validate_book(self, value):
        if value.inventory == 0:
            raise serializers.ValidationError("Book is not available for borrowing.")
        return value

    def create(self, validated_data):
        book = validated_data["book"]
        book.inventory -= 1
        book.save()
        borrowing = Borrowing.objects.create(
            book=book,
            borrower=self.context["request"].user,
        )
