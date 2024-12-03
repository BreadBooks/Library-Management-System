import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

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
    result_window = tk.Toplevel()  # Create a new top-level window
    result_window.title(title)

    tree = ttk.Treeview(result_window, columns=column_names, show='headings')
    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill=tk.BOTH, expand=True)

    for row in results:
        tree.insert('', tk.END, values=row)

# Main Application Class
class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("800x600")
        
        # Container for all pages
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (MainMenu, SearchPage, CheckoutPage, AddBorrowerPage, AddBookPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainMenu)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

# Main Menu Page
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="Library Management System", font=("Arial", 24)).pack(pady=40)
        
        tk.Button(self, text="Search Books", command=lambda: controller.show_frame(SearchPage), width=20).pack(pady=10)
        tk.Button(self, text="Checkout Book", command=lambda: controller.show_frame(CheckoutPage), width=20).pack(pady=10)
        tk.Button(self, text="Add Borrower", command=lambda: controller.show_frame(AddBorrowerPage), width=20).pack(pady=10)
        tk.Button(self, text="Add Book", command=lambda: controller.show_frame(AddBookPage), width=20).pack(pady=10)

# Search Page
class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="Search Books", font=("Arial", 18)).pack(pady=20)
        tk.Label(self, text="Enter Title, Author, or Keyword").pack()
        self.search_criteria_entry = tk.Entry(self)
        self.search_criteria_entry.pack(pady=5)
        
        tk.Button(self, text="Search", command=self.search_books).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=20)
    
    def search_books(self):
        search_criteria = self.search_criteria_entry.get()
        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            # Query books based on title, author, or keyword
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
class CheckoutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="Checkout Book", font=("Arial", 18)).pack(pady=20)
        tk.Label(self, text="Book ID").pack()
        self.book_id_entry = tk.Entry(self)
        self.book_id_entry.pack()
        tk.Label(self, text="Branch ID").pack()
        self.branch_id_entry = tk.Entry(self)
        self.branch_id_entry.pack()
        tk.Label(self, text="Card No").pack()
        self.card_no_entry = tk.Entry(self)
        self.card_no_entry.pack()
        tk.Button(self, text="Checkout", command=self.checkout_book).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=20)
    
    def checkout_book(self):
        book_id = self.book_id_entry.get()
        branch_id = self.branch_id_entry.get()
        card_no = self.card_no_entry.get()

        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            # Add to BOOK_LOANS
            cursor.execute("""
                INSERT INTO BOOK_LOANS (Book_Id, Branch_Id, Card_No, Date_Out, Due_Date)
                VALUES (%s, %s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY));
            """, (book_id, branch_id, card_no))

            # Fetch updated BOOK_COPIES
            cursor.execute("SELECT * FROM BOOK_COPIES WHERE Book_Id = %s AND Branch_Id = %s;", (book_id, branch_id))
            results = cursor.fetchall()
            conn.commit()

            column_names = [desc[0] for desc in cursor.description]
            display_results(results, column_names, "Updated Book Copies")
            messagebox.showinfo("Success", "Book checked out successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

# Add Borrower Page
class AddBorrowerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="Add Borrower", font=("Arial", 18)).pack(pady=20)
        tk.Label(self, text="Name").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()
        tk.Label(self, text="Address").pack()
        self.address_entry = tk.Entry(self)
        self.address_entry.pack()
        tk.Label(self, text="Phone").pack()
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack()
        tk.Button(self, text="Add Borrower", command=self.add_borrower).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=20)
    
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

# Add Book Page
class AddBookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="Add Book", font=("Arial", 18)).pack(pady=20)
        tk.Label(self, text="Title").pack()
        self.title_entry = tk.Entry(self)
        self.title_entry.pack()
        tk.Label(self, text="Publisher Name").pack()
        self.publisher_entry = tk.Entry(self)
        self.publisher_entry.pack()
        tk.Label(self, text="Author Name").pack()
        self.author_entry = tk.Entry(self)
        self.author_entry.pack()
        tk.Button(self, text="Add Book", command=self.add_book).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=20)
    
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
