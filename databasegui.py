import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import mysql.connector

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="meow",
        database="library_management"
    )

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("800x600")
        self.configure(fg_color="#bad7f5")  # Turquoise blue background

        # Define container for pages
        self.container = ctk.CTkFrame(self, fg_color="#bad7f5")
        self.container.pack(fill="both", expand=True)

        # Properly configure grid in container
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create a dictionary to store frames
        self.frames = {}

        # Initialize all pages
        for Page in (MainMenu, SearchPage, CheckoutPage, AddBorrowerPage, AddBookPage):
            page_name = Page.__name__
            frame = Page(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]
        frame.tkraise()


# Main Menu
class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#bad7f5")

        # Configure rows and columns for proper centering
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Logo Image
        logo_image = Image.open("book.png")
        logo = ctk.CTkImage(logo_image, size=(200, 200))
        logo_label = ctk.CTkLabel(self, text="", image=logo)
        logo_label.grid(row=0, column=0, pady=20)

        # Title
        title_label = ctk.CTkLabel(self, text="Library Management System", font=("Courier", 28, "bold"))
        title_label.grid(row=1, column=0, pady=10)

        # Buttons
        button_font = ("Courier", 20, "bold")
        button_frame = ctk.CTkFrame(self, fg_color="#bad7f5")  # Sub-frame for buttons
        button_frame.grid(row=2, column=0)

        ctk.CTkButton(button_frame, text="Search Books", fg_color="#635555", hover_color="#2e2626",
                      command=lambda: controller.show_frame("SearchPage"), font=button_font, width=200, height=50).pack(pady=10)
        ctk.CTkButton(button_frame, text="Checkout Book", fg_color="#635555", hover_color="#2e2626",
                      command=lambda: controller.show_frame("CheckoutPage"), font=button_font, width=200, height=50).pack(pady=10)
        ctk.CTkButton(button_frame, text="Add Borrower", fg_color="#635555", hover_color="#2e2626",
                      command=lambda: controller.show_frame("AddBorrowerPage"), font=button_font, width=200, height=50).pack(pady=10)
        ctk.CTkButton(button_frame, text="Add Book", fg_color="#635555", hover_color="#2e2626",
                      command=lambda: controller.show_frame("AddBookPage"), font=button_font, width=200, height=50).pack(pady=10)

# Search Page
class SearchPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#bad7f5")

        ctk.CTkLabel(self, text="Search Books", font=("Courier", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Enter Title, Author, or Keyword").pack(pady=10)

        self.search_criteria_entry = ctk.CTkEntry(self, width=300)
        self.search_criteria_entry.pack(pady=5)

        ctk.CTkButton(self, text="Search", command=self.search_books).pack(pady=10)
        ctk.CTkButton(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu")).pack(pady=10)

    def search_books(self):
        search_criteria = self.search_criteria_entry.get()
        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT b.Book_Id, b.Title, ba.Author_Name, b.Publisher_Name
                FROM BOOK b
                JOIN BOOK_AUTHORS ba ON b.Book_Id = ba.Book_Id
                WHERE b.Title LIKE %s OR ba.Author_Name LIKE %s;
            """, (f"%{search_criteria}%", f"%{search_criteria}%"))
            results = cursor.fetchall()

            if results:
                column_names = [desc[0] for desc in cursor.description]
                self.display_results(results, column_names)
            else:
                messagebox.showinfo("No Results", "No books found matching your search criteria.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    def display_results(self, results, column_names):
        result_window = ctk.CTkFrame(self, fg_color="#bad7f5")
        result_window.pack(fill="both", expand=True)
        tree = ctk.CTkTreeview(result_window, columns=column_names, show='headings')
        for col in column_names:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True, padx=20, pady=20)
        for row in results:
            tree.insert('', "end", values=row)

# Checkout Page
class CheckoutPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#bad7f5")

        ctk.CTkLabel(self, text="Checkout Book", font=("Courier", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Book ID").pack()
        self.book_id_entry = ctk.CTkEntry(self, width=300)
        self.book_id_entry.pack()

        ctk.CTkLabel(self, text="Branch ID").pack()
        self.branch_id_entry = ctk.CTkEntry(self, width=300)
        self.branch_id_entry.pack()

        ctk.CTkLabel(self, text="Card No").pack()
        self.card_no_entry = ctk.CTkEntry(self, width=300)
        self.card_no_entry.pack()

        ctk.CTkButton(self, text="Checkout", command=self.checkout_book).pack(pady=10)
        ctk.CTkButton(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu")).pack(pady=10)

    def checkout_book(self):
        # Your checkout implementation
        pass

# Add Borrower Page
class AddBorrowerPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#bad7f5")

        ctk.CTkLabel(self, text="Add Borrower", font=("Courier", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Name").pack(pady=5)
        self.name_entry = ctk.CTkEntry(self, width=300)
        self.name_entry.pack()

        ctk.CTkLabel(self, text="Address").pack(pady=5)
        self.address_entry = ctk.CTkEntry(self, width=300)
        self.address_entry.pack()

        ctk.CTkLabel(self, text="Phone").pack(pady=5)
        self.phone_entry = ctk.CTkEntry(self, width=300)
        self.phone_entry.pack()

        ctk.CTkButton(self, text="Add Borrower", command=self.add_borrower).pack(pady=10)
        ctk.CTkButton(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu")).pack(pady=10)

    def add_borrower(self):
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()

        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            # Insert into BORROWER
            cursor.execute("""
                INSERT INTO BORROWER (Name, Address, Phone)
                VALUES (%s, %s, %s);
            """, (name, address, phone))
            conn.commit()

            # Fetch the last inserted Card_No
            cursor.execute("SELECT LAST_INSERT_ID();")
            card_no = cursor.fetchone()[0]
            messagebox.showinfo("Success", f"Borrower added successfully! New Card No: {card_no}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

# Add Book Page (Similar to Add Borrower Page)
class AddBookPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#bad7f5")

        ctk.CTkLabel(self, text="Add Book", font=("Courier", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Title").pack(pady=5)
        self.title_entry = ctk.CTkEntry(self, width=300)
        self.title_entry.pack()

        ctk.CTkLabel(self, text="Publisher Name").pack(pady=5)
        self.publisher_entry = ctk.CTkEntry(self, width=300)
        self.publisher_entry.pack()

        ctk.CTkLabel(self, text="Author Name").pack(pady=5)
        self.author_entry = ctk.CTkEntry(self, width=300)
        self.author_entry.pack()

        ctk.CTkButton(self, text="Add Book", command=self.add_book).pack(pady=10)
        ctk.CTkButton(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu")).pack(pady=10)

    def add_book(self):
        title = self.title_entry.get()
        publisher = self.publisher_entry.get()
        author = self.author_entry.get()

        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            # Insert into BOOK
            cursor.execute("""
                INSERT INTO BOOK (Title, Publisher_Name)
                VALUES (%s, %s);
            """, (title, publisher))

            # Get the last inserted Book_Id
            cursor.execute("SELECT LAST_INSERT_ID();")
            book_id = cursor.fetchone()[0]

            # Insert into BOOK_AUTHORS
            cursor.execute("""
                INSERT INTO BOOK_AUTHORS (Book_Id, Author_Name)
                VALUES (%s, %s);
            """, (book_id, author))

            # Add 5 copies to all branches
            cursor.execute("SELECT Branch_Id FROM LIBRARY_BRANCH;")
            branches = cursor.fetchall()
            for branch in branches:
                cursor.execute("""
                    INSERT INTO BOOK_COPIES (Book_Id, Branch_Id, No_Of_Copies)
                    VALUES (%s, %s, 5);
                """, (book_id, branch[0]))
            conn.commit()
            messagebox.showinfo("Success", f"Book '{title}' added successfully with 5 copies in all branches.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

# Run the Application
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
