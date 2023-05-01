from rest_framework import serializers

from books.serializers import BookSerializer
from borrowing.models import Borrowing


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
        return borrowing
