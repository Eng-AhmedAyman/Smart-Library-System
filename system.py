import json
import os
from datetime import date, timedelta
from book import Book
from borrow_record import BorrowRecord


class LibrarySystem:
    def __init__(self, db_file="library_data.json", borrow_file="borrow.json"):
        self.db_file = db_file
        self.borrow_file = borrow_file
        self.books = []
        self.borrow_records = []

        self.load_data()
        self.load_borrow_data()

    # ---------------- Load/Save Books ----------------
    def load_data(self):
        if not os.path.exists(self.db_file):
            return
        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    book = Book(
                        item["title"],
                        item["author"],
                        item["isbn"],
                        item.get("borrow_man"),
                        item["is_available"],
                        item.get("borrow_date"),
                    )
                    self.books.append(book)
        except:
            self.books = []

    def save_data(self):
        data = [book.to_dict() for book in self.books]
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # ---------------- Load/Save Records ----------------
    def load_borrow_data(self):
        if not os.path.exists(self.borrow_file):
            return
        try:
            with open(self.borrow_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    rec = BorrowRecord(
                        item["isbn"],
                        item["user_id"],
                        item["name"],
                        item["phone"],
                        date.fromisoformat(item["borrow_date"]),
                        item["returned"],
                        item.get("fine", 0),  # 🔥 قراءة الغرامة
                    )
                    self.borrow_records.append(rec)
        except:
            self.borrow_records = []

    def save_borrow_data(self):
        data = [rec.to_dict() for rec in self.borrow_records]
        with open(self.borrow_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # ---------------- Operations ----------------
    def add_book(self, title, author, isbn):
        # 🔥 1. منع تكرار الـ ISBN
        if any(b.isbn == isbn for b in self.books):
            return False, "❌ Error: A book with this ISBN already exists!"

        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self.save_data()
        return True, "✅ Book Added Successfully!"

    def delete_book(self, isbn):
        # 🔥 2. حذف الكتاب (بشرط عدم الاستعارة)
        for book in self.books:
            if book.isbn == isbn:
                if not book.is_available:
                    return False, "⚠️ Cannot delete a borrowed book!\nReturn it first."

                self.books.remove(book)
                self.save_data()
                return True, "🗑️ Book Deleted Successfully."
        return False, "❌ Book not found."

    def borrow_book(self, isbn, user_id, name, phone):
        for book in self.books:
            if book.isbn == isbn:
                if not book.is_available:
                    return False, "❌ Book already borrowed."

                book.is_available = False
                book.borrow_man = name
                book.borrow_date = date.today()

                # إنشاء السجل
                rec = BorrowRecord(isbn, user_id, name, phone, date.today())
                self.borrow_records.append(rec)

                self.save_data()
                self.save_borrow_data()

                due_date = date.today() + timedelta(days=7)
                return True, f"✅ Borrowed Successfully!\n📅 Return by: {due_date}"

        return False, "❌ Book not found."

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.is_available:
                    return False, "⚠️ Book is not borrowed."

                msg = "🌟 Book returned successfully."
                fine_amount = 0

                # 🔥 3. حساب الغرامة
                if book.borrow_date:
                    days_diff = (date.today() - book.borrow_date).days
                    if days_diff > 7:
                        fine_amount = (days_diff - 7) * 50
                        msg = f"⚠️ LATE RETURN!\nOverdue: {days_diff - 7} days.\n💰 Fine Recorded: {fine_amount} EGP"

                # تصفير الكتاب
                book.is_available = True
                book.borrow_man = None
                book.borrow_date = None

                # تحديث السجل (إغلاق الاستعارة + تسجيل الغرامة)
                for rec in reversed(self.borrow_records):
                    if rec.isbn == isbn and not rec.returned:
                        rec.returned = True
                        rec.fine = fine_amount  # تسجيل الفلوس
                        break

                self.save_data()
                self.save_borrow_data()
                return True, msg

        return False, "❌ Book not found."
