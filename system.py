import json
import os
from datetime import date, timedelta
from book import Book  # استدعاء كلاس الكتاب من الملف الأول


class LibrarySystem:
    def __init__(self, db_file="library_data.json"):
        self.db_file = db_file
        self.books = []
        self.load_data()

    def add_book(self, title, author, isbn):
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self.save_data()
        return True

    def borrow_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.is_available:
                    book.is_available = False
                    book.borrow_date = date.today()
                    self.save_data()
                    return (
                        True,
                        f"✅ Borrowed: '{book.title}'\n📅 Return by: {book.borrow_date + timedelta(days=7)}",
                    )
                return False, "❌ Already borrowed."
        return False, "❌ Book not found."

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if not book.is_available:
                    returned_date = date.today()
                    # returned_date = date.today() + timedelta(days=20) # فك التعليق للتجربة
                    days_diff = (returned_date - book.borrow_date).days
                    msg = "🌟 Returned successfully."

                    if days_diff > 7:
                        fine = (days_diff - 7) * 50
                        msg = f"⚠️ LATE RETURN!\nOverdue: {days_diff - 7} days.\n💰 Fine: {fine} EGP"

                    book.is_available = True
                    book.borrow_date = None
                    self.save_data()
                    return True, msg
                return False, "⚠️ Not currently borrowed."
        return False, "❌ Book not found."

    def save_data(self):
        data = [book.to_dict() for book in self.books]
        with open(self.db_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if not os.path.exists(self.db_file):
            return
        try:
            with open(self.db_file, "r") as f:
                data = json.load(f)
                self.books = [Book(**item) for item in data]
        except:
            self.books = []
