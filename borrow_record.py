from datetime import date


class BorrowRecord:
    def __init__(self, isbn, user_id, name, phone, borrow_date, returned=False, fine=0):
        self.isbn = isbn
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.borrow_date = borrow_date
        self.returned = returned
        self.fine = fine  # 🔥 خانة الغرامة الجديدة

    def to_dict(self):
        return {
            "isbn": self.isbn,
            "user_id": self.user_id,
            "name": self.name,
            "phone": self.phone,
            "borrow_date": self.borrow_date.strftime("%Y-%m-%d"),
            "returned": self.returned,
            "fine": self.fine,  # 🔥 حفظ الغرامة
        }
