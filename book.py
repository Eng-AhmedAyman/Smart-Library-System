from datetime import datetime


class Book:
    def __init__(self, title, author, isbn, is_available=True, borrow_date=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = is_available
        if isinstance(borrow_date, str):
            try:
                self.borrow_date = datetime.strptime(borrow_date, "%Y-%m-%d").date()
            except ValueError:
                self.borrow_date = None
        else:
            self.borrow_date = borrow_date

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "is_available": self.is_available,
            "borrow_date": (
                self.borrow_date.strftime("%Y-%m-%d") if self.borrow_date else None
            ),
        }
