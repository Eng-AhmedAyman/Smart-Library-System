from datetime import datetime


class Book:
    def __init__(
        self,
        title,
        author,
        isbn,
        borrow_man=None,
        is_available=True,
        borrow_date=None,
    ):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = is_available
        self.borrow_man = borrow_man

        # تحويل التاريخ لو جاي String من JSON
        if isinstance(borrow_date, str):
            try:
                self.borrow_date = datetime.strptime(
                    borrow_date, "%Y-%m-%d"
                ).date()
            except ValueError:
                self.borrow_date = None
        else:
            self.borrow_date = borrow_date

    # ---------------- Convert to JSON ----------------
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "is_available": self.is_available,
            "borrow_man": self.borrow_man,
            "borrow_date": self.borrow_date.strftime("%Y-%m-%d")
            if self.borrow_date
            else None,
        }
