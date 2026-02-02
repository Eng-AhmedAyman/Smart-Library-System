from datetime import datetime

class Book:
    """
    Represents the data model for a book in the library.
    
    Attributes:
        title (str): The name of the book.
        author (str): The author of the book.
        isbn (str): Unique identifier (International Standard Book Number).
        borrow_man (str, optional): Name of the borrower if not available.
        is_available (bool): Status indicating if the book can be borrowed.
        borrow_date (date, optional): The date the book was issued.
    """
    def __init__(self, title, author, isbn, borrow_man=None, is_available=True, borrow_date=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = is_available
        self.borrow_man = borrow_man

        # Convert date from string (JSON format) to Python date object if necessary
        if isinstance(borrow_date, str):
            try:
                self.borrow_date = datetime.strptime(borrow_date, "%Y-%m-%d").date()
            except ValueError:
                self.borrow_date = None
        else:
            self.borrow_date = borrow_date

    def to_dict(self):
        """
        Serializes the Book object into a dictionary for JSON storage.
        
        Returns:
            dict: A dictionary containing book attributes.
        """
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "is_available": self.is_available,
            "borrow_man": self.borrow_man,
            "borrow_date": self.borrow_date.strftime("%Y-%m-%d") if self.borrow_date else None,
        }
