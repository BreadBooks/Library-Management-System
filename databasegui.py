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
        button_font = ("Courier", 22, "bold")
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
        
# Helper Functions for Styling
def styled_entry(parent, width=400):
    """Create a styled CTkEntry."""
    return ctk.CTkEntry(parent, width=width, font=("Courier", 16))

def styled_button(parent, text, command):
    """Create a styled CTkButton."""
    return ctk.CTkButton(
        parent,
        text=text,
        fg_color="#635555",
        hover_color="#2e2626",
        font=("Courier", 20, "bold"),
        width=200,
        height=50,
        command=command,
    )
    
# Search Page
class SearchPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#bad7f5")

        # Centering Content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Content Frame
        content_frame = ctk.CTkFrame(self, fg_color="#bad7f5")
        content_frame.grid(row=0, column=0, sticky="nsew")

        # Header
        ctk.CTkLabel(content_frame, text="Search Books", font=("Courier", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(content_frame, text="Enter Title, Author, or Keyword", font=("Courier", 16)).pack(pady=10)

        # Input Field
        self.search_criteria_entry = styled_entry(content_frame)
        self.search_criteria_entry.pack(pady=10)

        # Buttons
        styled_button(content_frame, "Search", self.search_books).pack(pady=10)
        styled_button(content_frame, "Back to Main Menu", lambda: controller.show_frame("MainMenu")).pack(pady=10)

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

        # Centering Content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Content Frame
        content_frame = ctk.CTkFrame(self, fg_color="#bad7f5")
        content_frame.grid(row=0, column=0, sticky="nsew")

        # Header
        ctk.CTkLabel(content_frame, text="Checkout Book", font=("Courier", 24, "bold")).pack(pady=20)

        # Input Fields
        ctk.CTkLabel(content_frame, text="Book ID", font=("Courier", 16)).pack(pady=5)
        self.book_id_entry = styled_entry(content_frame)
        self.book_id_entry.pack(pady=5)

        ctk.CTkLabel(content_frame, text="Branch ID", font=("Courier", 16)).pack(pady=5)
        self.branch_id_entry = styled_entry(content_frame)
        self.branch_id_entry.pack(pady=5)

        ctk.CTkLabel(content_frame, text="Card No", font=("Courier", 16)).pack(pady=5)
        self.card_no_entry = styled_entry(content_frame)
        self.card_no_entry.pack(pady=5)

        # Buttons
        styled_button(content_frame, "Checkout", self.checkout_book).pack(pady=10)
        styled_button(content_frame, "Back to Main Menu", lambda: controller.show_frame("MainMenu")).pack(pady=10)

    def checkout_book(self):
        """Handles the book checkout process."""
        book_id = self.book_id_entry.get().strip()
        branch_id = self.branch_id_entry.get().strip()
        card_no = self.card_no_entry.get().strip()

        # Validation
        if not book_id or not branch_id or not card_no:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            # Insert into BOOK_LOANS
            cursor.execute("""
                INSERT INTO BOOK_LOANS (Book_Id, Branch_Id, Card_No, Date_Out, Due_Date)
                VALUES (%s, %s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY));
            """, (book_id, branch_id, card_no))

            # Fetch updated BOOK_COPIES
            cursor.execute("SELECT * FROM BOOK_COPIES WHERE Book_Id = %s AND Branch_Id = %s;", (book_id, branch_id))
            results = cursor.fetchall()

            if not results:
                messagebox.showerror("Error", "Book or branch not found, or no copies available!")
                conn.rollback()
                return

            conn.commit()
            column_names = [desc[0] for desc in cursor.description]
            self.display_results(results, column_names)
            messagebox.showinfo("Success", "Book checked out successfully!")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    def display_results(self, results, column_names):
        """Displays updated book copies in a new window."""
        result_window = ctk.CTkToplevel(self)
        result_window.title("Updated Book Copies")
        result_window.geometry("600x400")
        tree = ctk.CTkTreeview(result_window, columns=column_names, show='headings')
        for col in column_names:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True, padx=20, pady=20)
        for row in results:
            tree.insert('', "end", values=row)


# Add Borrower Page
class AddBorrowerPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)  # Initialize parent class
        self.controller = controller
        self.configure(fg_color="#bad7f5")

        # Centering Content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Content Frame
        content_frame = ctk.CTkFrame(self, fg_color="#bad7f5")
        content_frame.grid(row=0, column=0, sticky="nsew")

        # Header
        ctk.CTkLabel(content_frame, text="Add Borrower", font=("Courier", 24, "bold")).pack(pady=20)

        # Input Fields
        ctk.CTkLabel(content_frame, text="Name", font=("Courier", 16)).pack(pady=5)
        self.name_entry = styled_entry(content_frame)
        self.name_entry.pack(pady=5)

        ctk.CTkLabel(content_frame, text="Address", font=("Courier", 16)).pack(pady=5)
        self.address_entry = styled_entry(content_frame)
        self.address_entry.pack(pady=5)

        ctk.CTkLabel(content_frame, text="Phone", font=("Courier", 16)).pack(pady=5)
        self.phone_entry = styled_entry(content_frame)
        self.phone_entry.pack(pady=5)

        # Buttons
        styled_button(content_frame, "Add Borrower", self.add_borrower).pack(pady=10)
        styled_button(content_frame, "Back to Main Menu", lambda: controller.show_frame("MainMenu")).pack(pady=10)

    def add_borrower(self):
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()

        if not name or not address or not phone:
            messagebox.showerror("Error", "All fields are required!")
            return

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
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

# Add Book Page (Similar to Add Borrower Page)
class AddBookPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)  # Initialize parent class
        self.controller = controller
        self.configure(fg_color="#bad7f5")

        # Centering Content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Content Frame
        content_frame = ctk.CTkFrame(self, fg_color="#bad7f5")
        content_frame.grid(row=0, column=0, sticky="nsew")

        # Header
        ctk.CTkLabel(content_frame, text="Add Book", font=("Courier", 24, "bold")).pack(pady=20)

        # Input Fields
        ctk.CTkLabel(content_frame, text="Title", font=("Courier", 16)).pack(pady=5)
        self.title_entry = styled_entry(content_frame)
        self.title_entry.pack(pady=5)

        ctk.CTkLabel(content_frame, text="Publisher Name", font=("Courier", 16)).pack(pady=5)
        self.publisher_entry = styled_entry(content_frame)
        self.publisher_entry.pack(pady=5)

        ctk.CTkLabel(content_frame, text="Author Name", font=("Courier", 16)).pack(pady=5)
        self.author_entry = styled_entry(content_frame)
        self.author_entry.pack(pady=5)

        # Buttons
        styled_button(content_frame, "Add Book", self.add_book).pack(pady=10)
        styled_button(content_frame, "Back to Main Menu", lambda: controller.show_frame("MainMenu")).pack(pady=10)

    def add_book(self):
        """Handles the book addition process."""
        title = self.title_entry.get().strip()
        publisher = self.publisher_entry.get().strip()
        author = self.author_entry.get().strip()

        # Validation
        if not title or not publisher or not author:
            messagebox.showerror("Error", "All fields are required!")
            return

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
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

# Run the Application
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
