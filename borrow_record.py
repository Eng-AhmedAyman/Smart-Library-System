from datetime import date

class BorrowRecord:
    """
    Represents a historical or active borrowing transaction.
    
    Attributes:
        isbn (str): ISBN of the borrowed book.
        user_id (str): Unique identifier for the borrower.
        name (str): Full name of the borrower.
        phone (str): Contact phone number of the borrower.
        borrow_date (date): The date the transaction occurred.
        returned (bool): Status indicating if the book has been returned.
        fine (float): The total overdue fine calculated at return.
    """
    def __init__(self, isbn, user_id, name, phone, borrow_date, returned=False, fine=0):
        self.isbn = isbn
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.borrow_date = borrow_date
        self.returned = returned
        self.fine = fine

    def to_dict(self):
        """
        Converts the record into a dictionary format for JSON persistence.
        
        Returns:
            dict: The serialized borrow record.
        """
        return {
            "isbn": self.isbn,
            "user_id": self.user_id,
            "name": self.name,
            "phone": self.phone,
            "borrow_date": self.borrow_date.strftime("%Y-%m-%d"),
            "returned": self.returned,
            "fine": self.fine,
        }
