import customtkinter as ctk
from tkinter import messagebox
from datetime import date, timedelta
from system import LibrarySystem
from PIL import Image, ImageTk

# Standard Theme Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class LibraryApp(ctk.CTk):
    """
    Main Application Class for the Smart Library Management System.
    Handles the GUI layout, navigation between views, and user interactions.
    """

    def __init__(self):
        super().__init__()

        self.title("Smart Library System📚")
        self.geometry("1150x700")
        self.library = LibrarySystem()

        # --- Application Icon (Logo) Setup ---
        try:
            icon_img = Image.open("logoo.jpg")
            self.iconphoto(False, ImageTk.PhotoImage(icon_img))
        except Exception:
            pass

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------- Sidebar Navigation ----------
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Sidebar Logo Display
        try:
            my_image = ctk.CTkImage(
                light_image=Image.open("logoo.jpg"),
                dark_image=Image.open("logoo.jpg"),
                size=(100, 100),
            )
            ctk.CTkLabel(self.sidebar, text="", image=my_image).pack(pady=(30, 10))
        except Exception:
            pass

        ctk.CTkLabel(
            self.sidebar,
            text="Smart Lib System",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(0, 20))

        # Navigation Buttons
        self.add_nav_btn("Dashboard", "dashboard")
        self.add_nav_btn("Add Books", "manage")
        self.add_nav_btn("Smart Scanner", "borrow")
        self.add_nav_btn("Borrowers Log", "borrowers")

        # ---------- Main Content Area ----------
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.show_frame("dashboard")

    # ---------- Navigation Logic ----------
    def add_nav_btn(self, text, view):
        """Creates a standardized navigation button in the sidebar."""
        ctk.CTkButton(
            self.sidebar,
            text=text,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            hover_color=("#3B8ED0", "#1f538d"),
            command=lambda: self.show_frame(view),
        ).pack(pady=10, padx=20, fill="x")

    def show_frame(self, name):
        """Clears the main frame and switches to the requested view."""
        for w in self.main_frame.winfo_children():
            w.destroy()
        if name == "dashboard":
            self.create_dashboard()
        elif name == "manage":
            self.create_manage()
        elif name == "borrow":
            self.create_borrow()
        elif name == "borrowers":
            self.create_borrowers()

    # ---------- Dashboard View ----------
    def create_dashboard(self):
        """Constructs the dashboard view with live statistics and a searchable book list."""
        top = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top.pack(fill="x", pady=10, padx=20)

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
        self.stats_area.pack(fill="x", pady=10, padx=20)
        self.refresh_stats()

        # Policy Notification Bar
        policy_frame = ctk.CTkFrame(
            self.main_frame, fg_color="#4a2c04", corner_radius=5, height=35
        )
        policy_frame.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(
            policy_frame,
            text="⚠️ Policy: 7-Day Loan Period | 💰 Late Fine: 50 EGP per day delayed.",
            text_color="#ffb84d",
            font=("Arial", 12, "bold"),
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Table Header
        cols = ctk.CTkFrame(self.main_frame, height=35, fg_color="#2b2b2b")
        cols.pack(fill="x", pady=5, padx=20)
        headers = [
            ("ISBN", 80),
            ("Title", 230),
            ("Author", 130),
            ("Status / Fine", 210),
            ("Action", 120),
        ]
        for txt, w in headers:
            ctk.CTkLabel(
                cols, text=txt, width=w, anchor="w", font=("Arial", 12, "bold")
            ).pack(side="left", padx=5)

        self.scroll = ctk.CTkScrollableFrame(self.main_frame)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)
        self.update_list()

    def refresh_stats(self):
        """Calculates and refreshes library totals and availability metrics."""
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
            ctk.CTkLabel(card, text=title, font=("Arial", 14, "bold")).place(
                relx=0.5, rely=0.3, anchor="center"
            )
            ctk.CTkLabel(
                card, text=str(val), font=("Arial", 24, "bold"), text_color="white"
            ).place(relx=0.5, rely=0.7, anchor="center")

    def update_list(self, *args):
        """Filters the book list based on user search queries."""
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
        """Renders an individual book row with status indicators and action buttons."""
        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.pack(fill="x", pady=4, padx=5)

        display_title = book.title[:27] + "..." if len(book.title) > 30 else book.title
        display_author = (
            book.author[:15] + "..." if len(book.author) > 18 else book.author
        )

        ctk.CTkLabel(row, text=book.isbn, width=80, anchor="w").pack(
            side="left", padx=5
        )
        ctk.CTkLabel(
            row, text=display_title, width=230, anchor="w", font=("Arial", 13, "bold")
        ).pack(side="left", padx=5)
        ctk.CTkLabel(row, text=display_author, width=130, anchor="w").pack(
            side="left", padx=5
        )

        # Dynamic Status and Fine Calculation
        if book.is_available:
            status_txt, status_col = "🟢 Available", "#2cc985"
        else:
            due_date = (
                book.borrow_date + timedelta(days=7)
                if book.borrow_date
                else date.today()
            )
            days_left = (due_date - date.today()).days
            if days_left < 0:
                fine = abs(days_left) * 50
                status_txt = f"🔴 LATE ({abs(days_left)}d) | Pay: {fine}"
                status_col = "#ff4d4d"
            else:
                status_txt = f"📅 Due: {due_date}"
                status_col = "#ffa500"

        ctk.CTkLabel(
            row,
            text=status_txt,
            text_color=status_col,
            width=210,
            anchor="w",
            font=("Arial", 12, "bold"),
        ).pack(side="left", padx=5)

        # Action Buttons (Borrow/Return and Delete)
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.pack(side="left", padx=5)

        btn_txt = "Borrow" if book.is_available else "Return"
        btn_col = "#2cc985" if book.is_available else "#c92c2c"
        ctk.CTkButton(
            actions_frame,
            text=btn_txt,
            width=70,
            fg_color=btn_col,
            command=lambda b=book: self.quick_action(b),
        ).pack(side="left", padx=2)
        ctk.CTkButton(
            actions_frame,
            text="X",
            width=30,
            fg_color="#444",
            hover_color="#800000",
            command=lambda b=book: self.delete_action(b),
        ).pack(side="left", padx=2)

    def delete_action(self, book):
        """Prompts user for deletion and removes the book from the library database."""
        if messagebox.askyesno(
            "Delete", f"Are you sure you want to delete '{book.title}'?"
        ):
            ok, msg = self.library.delete_book(book.isbn)
            if ok:
                messagebox.showinfo("Deleted", msg)
                self.refresh_ui()
            else:
                messagebox.showerror("Error", msg)

    def quick_action(self, book):
        """Handles immediate borrow/return logic, including overdue fine confirmation."""
        if book.is_available:
            self.borrow_popup(book)
        else:
            due_date = (
                book.borrow_date + timedelta(days=7)
                if book.borrow_date
                else date.today()
            )
            days_left = (due_date - date.today()).days
            if days_left < 0:
                fine = abs(days_left) * 50
                confirm = messagebox.askyesno(
                    "💰 Fine Payment",
                    f"User is late by {abs(days_left)} days.\nFine Amount: {fine} EGP\n\nHas the user paid?",
                )
                if not confirm:
                    return

            if messagebox.askyesno("Confirm", f"Return '{book.title}'?"):
                ok, msg = self.library.return_book(book.isbn)
                messagebox.showinfo("Done", msg)
                self.refresh_ui()

    def borrow_popup(self, book):
        """Opens a top-level window to gather borrower details with auto-incrementing ID."""
        win = ctk.CTkToplevel(self)
        win.geometry("400x400")
        win.title("Borrow Details")
        win.attributes("-topmost", True)
        ctk.CTkLabel(
            win, text=f"Borrowing: {book.title}", font=("Arial", 16, "bold")
        ).pack(pady=20)

        next_id = 101
        ids = [
            int(r.user_id)
            for r in self.library.borrow_records
            if str(r.user_id).isdigit()
        ]
        if ids:
            next_id = max(ids) + 1

        entries = []
        for p in ["User ID", "Borrower Name", "Phone (11 digits)"]:
            e = ctk.CTkEntry(win, placeholder_text=p, width=300)
            e.pack(pady=10)
            if p == "User ID":
                e.insert(0, str(next_id))
            entries.append(e)

        def confirm():
            uid, name, phone = entries[0].get(), entries[1].get(), entries[2].get()
            if not (uid and name and phone):
                messagebox.showerror("Error", "Required!")
                return
            if not phone.isdigit() or len(phone) != 11:
                messagebox.showerror("Error", "Invalid Phone!")
                return
            ok, msg = self.library.borrow_book(book.isbn, uid, name, phone)
            messagebox.showinfo("Result", msg)
            win.destroy()
            self.refresh_ui()

        ctk.CTkButton(win, text="Confirm", fg_color="green", command=confirm).pack(
            pady=20
        )

    def refresh_ui(self):
        """Refreshes statistics and lists across the UI."""
        self.refresh_stats()
        self.update_list()

    # ---------- Manage Books View ----------
    def create_manage(self):
        """Interface for manually adding new book records to the library."""
        ctk.CTkLabel(self.main_frame, text="Add New Book", font=("Arial", 24)).pack(
            pady=20
        )
        self.e_t = ctk.CTkEntry(self.main_frame, placeholder_text="Title", width=300)
        self.e_t.pack(pady=5)
        self.e_a = ctk.CTkEntry(self.main_frame, placeholder_text="Author", width=300)
        self.e_a.pack(pady=5)
        self.e_i = ctk.CTkEntry(self.main_frame, placeholder_text="ISBN", width=300)
        self.e_i.pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Save Book", command=self.save_book).pack(
            pady=20
        )

    def save_book(self):
        """Validates and saves a new book via the LibrarySystem controller."""
        if self.e_t.get() and self.e_i.get():
            ok, msg = self.library.add_book(
                self.e_t.get(), self.e_a.get(), self.e_i.get()
            )
            if ok:
                messagebox.showinfo("Success", msg)
                self.refresh_ui()
            else:
                messagebox.showerror("Error", msg)
        else:
            messagebox.showwarning("Error", "Missing Data")

    # ---------- Smart ISBN Scanner View ----------
    def create_borrow(self):
        """Initializes the intelligent scanning interface for quick borrow/return operations."""
        ctk.CTkLabel(
            self.main_frame, text="🔫 Smart ISBN Scanner", font=("Arial", 24, "bold")
        ).pack(pady=20)
        ctk.CTkLabel(
            self.main_frame,
            text="Scan or Type ISBN to Borrow/Return automatically:",
            font=("Arial", 14),
            text_color="gray",
        ).pack(pady=(0, 10))

        self.scan_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter ISBN here...",
            width=400,
            height=40,
            font=("Arial", 16),
        )
        self.scan_entry.pack(pady=15)
        self.scan_entry.bind("<Return>", lambda event: self.scan_action())

        ctk.CTkButton(
            self.main_frame,
            text="🚀 Process Action",
            width=200,
            height=40,
            fg_color="#3B8ED0",
            font=("Arial", 14, "bold"),
            command=self.scan_action,
        ).pack(pady=10)
        self.status_label = ctk.CTkLabel(
            self.main_frame, text="", font=("Arial", 14, "bold")
        )
        self.status_label.pack(pady=20)

    def scan_action(self):
        """Processes the scanned ISBN and triggers the correct flow (Borrow/Return)."""
        isbn = self.scan_entry.get().strip()
        if not isbn:
            messagebox.showwarning("Warning", "Enter ISBN!")
            return

        book = next((b for b in self.library.books if b.isbn == isbn), None)
        if not book:
            self.status_label.configure(
                text=f"❌ Book '{isbn}' not found!", text_color="#ff4d4d"
            )
            self.bell()
            return

        self.scan_entry.delete(0, "end")
        if book.is_available:
            self.status_label.configure(
                text=f"📖 '{book.title}' is Available. Opening Borrow...",
                text_color="#2cc985",
            )
            self.borrow_popup(book)
        else:
            self.status_label.configure(
                text=f"🔄 '{book.title}' is Borrowed. Return Process...",
                text_color="#ffa500",
            )
            self.quick_action(book)

    # ---------- Transaction Logs (Audit View) ----------
    def create_borrowers(self):
        """Renders the historical audit log of all borrowing and returning transactions."""
        ctk.CTkLabel(
            self.main_frame, text="📜 Borrowing History Log", font=("Arial", 24, "bold")
        ).pack(pady=20)
        header_frame = ctk.CTkFrame(self.main_frame, height=40, fg_color="#2b2b2b")
        header_frame.pack(fill="x", padx=20, pady=5)

        headers = [
            ("ID", 50),
            ("Borrower", 130),
            ("Phone", 100),
            ("Book Title", 180),
            ("Date", 90),
            ("Fine", 70),
            ("Status", 90),
        ]
        for txt, w in headers:
            ctk.CTkLabel(
                header_frame,
                text=txt,
                width=w,
                anchor="w",
                font=("Arial", 12, "bold"),
                text_color="white",
            ).pack(side="left", padx=5)

        scroll = ctk.CTkScrollableFrame(self.main_frame)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        for rec in reversed(self.library.borrow_records):
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=2, padx=5)
            book_obj = next((b for b in self.library.books if b.isbn == rec.isbn), None)
            b_title = (
                book_obj.title[:20] + "..."
                if book_obj and len(book_obj.title) > 23
                else (book_obj.title if book_obj else "Unknown")
            )

            status_txt, status_col = (
                ("✅ Returned", "#2cc985") if rec.returned else ("🟠 Active", "#ffa500")
            )
            fine_txt, fine_col = (
                (f"{rec.fine} EGP", "#ff4d4d") if rec.fine > 0 else ("-", "white")
            )

            data = [
                (str(rec.user_id), 50),
                (rec.name, 130),
                (rec.phone, 100),
                (b_title, 180),
                (str(rec.borrow_date), 90),
            ]
            for txt, w in data:
                ctk.CTkLabel(row, text=txt, width=w, anchor="w").pack(
                    side="left", padx=5
                )
            ctk.CTkLabel(
                row,
                text=fine_txt,
                text_color=fine_col,
                width=70,
                anchor="w",
                font=("Arial", 11, "bold"),
            ).pack(side="left", padx=5)
            ctk.CTkLabel(
                row,
                text=status_txt,
                text_color=status_col,
                width=90,
                anchor="w",
                font=("Arial", 11, "bold"),
            ).pack(side="left", padx=5)
