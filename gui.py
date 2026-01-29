import customtkinter as ctk
from tkinter import messagebox
from datetime import date, timedelta
from system import LibrarySystem  # ربطنا الواجهة بالسيستم

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Smart Library System📚")
        self.geometry("1100x700")
        self.library = LibrarySystem()  # هنا عملنا نسخة من السيستم

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            self.sidebar, text="📚 Smart Lib", font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=30)

        self.add_nav_btn("Dashboard", "dashboard")
        self.add_nav_btn("Add Books", "manage")
        self.add_nav_btn("Manual Scan", "borrow")

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.show_frame("dashboard")

    def add_nav_btn(self, text, view):
        ctk.CTkButton(
            self.sidebar, text=text, command=lambda: self.show_frame(view)
        ).pack(pady=10, padx=20)

    def show_frame(self, name):
        for w in self.main_frame.winfo_children():
            w.destroy()
        if name == "dashboard":
            self.create_dashboard()
        elif name == "manage":
            self.create_manage()
        elif name == "borrow":
            self.create_borrow()

    def create_dashboard(self):
        top = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top.pack(fill="x", pady=10)
        ctk.CTkLabel(top, text="Library Dashboard", font=("Arial", 26, "bold")).pack(
            side="left"
        )

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.update_list)
        ctk.CTkEntry(
            top,
            placeholder_text="🔍 Search Title, Author or ISBN...",
            textvariable=self.search_var,
            width=300,
        ).pack(side="right")

        self.stats_area = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.stats_area.pack(fill="x", pady=10)
        self.refresh_stats()

        info_frame = ctk.CTkFrame(
            self.main_frame, fg_color="#3a3a3a", height=30, corner_radius=5
        )
        info_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(
            info_frame,
            text="ℹ️ Policy: 7-Day Loan Period | ⚠️ Late Fine: 50 EGP/day",
            text_color="#ffb84d",
            font=("Arial", 13, "bold"),
        ).pack(pady=5)

        cols = ctk.CTkFrame(self.main_frame, height=35, fg_color="#2b2b2b")
        cols.pack(fill="x", pady=5)
        headers = [
            ("ISBN", 100),
            ("Title", 220),
            ("Author", 150),
            ("Status / Due Date", 180),
            ("Action", 80),
        ]
        for txt, w in headers:
            ctk.CTkLabel(
                cols, text=txt, width=w, anchor="w", font=("Arial", 12, "bold")
            ).pack(side="left", padx=5)

        self.scroll = ctk.CTkScrollableFrame(self.main_frame, width=900, height=350)
        self.scroll.pack(fill="both", expand=True)
        self.update_list()

    def refresh_stats(self):
        for w in self.stats_area.winfo_children():
            w.destroy()
        total = len(self.library.books)
        avail = sum(1 for b in self.library.books if b.is_available)
        borrowed = total - avail
        for title, val, col in [
            ("Total Books", total, "#1f538d"),
            ("Available", avail, "#2cc985"),
            ("Borrowed", borrowed, "#c92c2c"),
        ]:
            card = ctk.CTkFrame(self.stats_area, width=180, height=80, fg_color=col)
            card.pack(side="left", padx=10, expand=True)
            ctk.CTkLabel(card, text=title).place(relx=0.5, rely=0.3, anchor="center")
            ctk.CTkLabel(card, text=str(val), font=("Arial", 24, "bold")).place(
                relx=0.5, rely=0.7, anchor="center"
            )

    def update_list(self, *args):
        for w in self.scroll.winfo_children():
            w.destroy()
        term = self.search_var.get().lower()
        for book in self.library.books:
            if (
                term in book.title.lower()
                or term in book.author.lower()
                or term in book.isbn
            ):
                self.draw_row(book)

    def draw_row(self, book):
        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.pack(fill="x", pady=4)
        ctk.CTkLabel(
            row, text=book.isbn, width=100, anchor="w", font=("Consolas", 12)
        ).pack(side="left", padx=5)
        ctk.CTkLabel(
            row, text=book.title, width=220, anchor="w", font=("Arial", 13, "bold")
        ).pack(side="left", padx=5)
        ctk.CTkLabel(row, text=book.author, width=150, anchor="w").pack(
            side="left", padx=5
        )

        if book.is_available:
            status_txt, status_col = "🟢 Available", "#2cc985"
        else:
            due_date = book.borrow_date + timedelta(days=7)
            days_left = (due_date - date.today()).days
            status_txt = (
                f"⚠️ LATE ({abs(days_left)} days)"
                if days_left < 0
                else f"📅 Due: {due_date}"
            )
            status_col = "#ff4d4d" if days_left < 0 else "#ffb84d"

        ctk.CTkLabel(
            row, text=status_txt, text_color=status_col, width=180, anchor="w"
        ).pack(side="left", padx=5)

        if book.is_available:
            ctk.CTkButton(
                row,
                text="Borrow",
                width=80,
                height=25,
                fg_color="#2cc985",
                hover_color="green",
                command=lambda b=book: self.quick_action(b, "borrow"),
            ).pack(side="left", padx=5)
        else:
            ctk.CTkButton(
                row,
                text="Return",
                width=80,
                height=25,
                fg_color="#c92c2c",
                hover_color="darkred",
                command=lambda b=book: self.quick_action(b, "return"),
            ).pack(side="left", padx=5)

    def quick_action(self, book, action):
        if action == "borrow":
            if messagebox.askyesno("Confirm", f"Borrow '{book.title}'?"):
                ok, msg = self.library.borrow_book(book.isbn)
                if ok:
                    self.refresh_ui()
                else:
                    messagebox.showerror("Error", msg)
        else:
            if messagebox.askyesno("Confirm", f"Return '{book.title}'?"):
                ok, msg = self.library.return_book(book.isbn)
                if ok:
                    self.refresh_ui()
                    if "Fine" in msg:
                        messagebox.showwarning("Late Return", msg)
                    else:
                        messagebox.showinfo("Done", msg)

    def refresh_ui(self):
        self.refresh_stats()
        self.update_list()

    def create_manage(self):
        ctk.CTkLabel(self.main_frame, text="Add New Book", font=("Arial", 24)).pack(
            pady=20
        )
        self.e_t = ctk.CTkEntry(self.main_frame, placeholder_text="Title", width=300)
        self.e_t.pack(pady=5)
        self.e_a = ctk.CTkEntry(self.main_frame, placeholder_text="Author", width=300)
        self.e_a.pack(pady=5)
        self.e_i = ctk.CTkEntry(self.main_frame, placeholder_text="ISBN", width=300)
        self.e_i.pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Save", command=self.save_book).pack(
            pady=20
        )

    def save_book(self):
        if self.e_t.get() and self.e_a.get() and self.e_i.get():
            self.library.add_book(self.e_t.get(), self.e_a.get(), self.e_i.get())
            messagebox.showinfo("Success", "Book Added!")
            self.e_t.delete(0, "end")
            self.e_a.delete(0, "end")
            self.e_i.delete(0, "end")
        else:
            messagebox.showwarning("Empty", "Fill fields!")

    def create_borrow(self):
        ctk.CTkLabel(self.main_frame, text="Manual Scan", font=("Arial", 24)).pack(
            pady=20
        )
        self.scan_entry = ctk.CTkEntry(
            self.main_frame, placeholder_text="Enter ISBN", width=300
        )
        self.scan_entry.pack(pady=20)
        btn_box = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_box.pack()
        ctk.CTkButton(
            btn_box,
            text="Borrow",
            fg_color="green",
            command=lambda: self.scan_act("borrow"),
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            btn_box,
            text="Return",
            fg_color="red",
            command=lambda: self.scan_act("return"),
        ).pack(side="left", padx=10)

    def scan_act(self, act):
        isbn = self.scan_entry.get()
        ok, msg = (
            self.library.borrow_book(isbn)
            if act == "borrow"
            else self.library.return_book(isbn)
        )
        if ok:
            messagebox.showinfo("Info", msg)
            self.scan_entry.delete(0, "end")
        else:
            messagebox.showerror("Error", msg)
