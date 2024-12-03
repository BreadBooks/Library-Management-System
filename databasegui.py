import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from PIL import Image

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="meow",
        database="library_management"
    )

# Helper Function to Display Results in a Treeview
def display_results(results, column_names, title="Results"):
    result_window = ctk.CTkToplevel()  # Create a new top-level window
    result_window.title(title)
    result_window.geometry("600x400")

    tree = ctk.CTkTreeview(result_window, columns=column_names, show='headings')
    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True, padx=20, pady=20)

    for row in results:
        tree.insert('', "end", values=row)

# Main Application Class
class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("800x600")
        self.configure(fg_color="#66d9e8")  # Set background to turquoise blue

        # Logo Image
        self.logo_image = Image.open("book.png")  # Load the logo image
        self.logo = ctk.CTkImage(self.logo_image, size=(200, 200))
        logo_label = ctk.CTkLabel(self, text="", image=self.logo)
        logo_label.pack(pady=10)

        # Title
        title_label = ctk.CTkLabel(self, text="Library Management System", font=("Courier", 28, "bold"))
        title_label.pack(pady=20)

         # Buttons for Navigation
        button_font = ("Courier", 20, "bold")  # Bold Font for Buttons

        ctk.CTkButton(self, text="Search Books", command=self.open_search_page, font=button_font, width=200, height=50).pack(pady=10)
        ctk.CTkButton(self, text="Checkout Book", command=self.open_checkout_page, font=button_font, width=200, height=50).pack(pady=10)
        ctk.CTkButton(self, text="Add Borrower", command=self.open_add_borrower_page, font=button_font, width=200, height=50).pack(pady=10)
        ctk.CTkButton(self, text="Add Book", command=self.open_add_book_page, font=button_font, width=200, height=50).pack(pady=10)

    def open_search_page(self):
        SearchPage(self)

    def open_checkout_page(self):
        CheckoutPage(self)

    def open_add_borrower_page(self):
        AddBorrowerPage(self)

    def open_add_book_page(self):
        AddBookPage(self)

# Search Page
class SearchPage(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("600x400")
        self.configure(fg_color="#66d9e8")
        self.title("Search Books")

        ctk.CTkLabel(self, text="Search Books", font=("Courier", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Enter Title, Author, or Keyword").pack(pady=10)

        self.search_criteria_entry = ctk.CTkEntry(self, width=300)
        self.search_criteria_entry.pack(pady=5)

        ctk.CTkButton(self, text="Search", command=self.search_books).pack(pady=10)

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
                display_results(results, column_names, "Search Results")
            else:
                messagebox.showinfo("No Results", "No books found matching your search criteria.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

# Checkout Page
class CheckoutPage(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("600x400")
        self.configure(fg_color="#66d9e8")
        self.title("Checkout Book")

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

    def checkout_book(self):
        # (Implementation for checkout similar to your original code)
        pass

# Add Borrower Page (Similar to Search and Checkout)
class AddBorrowerPage(ctk.CTkToplevel):
    pass

# Add Book Page (Similar to Search and Checkout)
class AddBookPage(ctk.CTkToplevel):
    pass

# Run the Application
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
