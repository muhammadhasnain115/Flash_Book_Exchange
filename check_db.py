from app.models import Book
b = Book.query.first()
print(b.image_file)
