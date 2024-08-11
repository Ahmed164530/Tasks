class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.checked_out = False

    def __str__(self):
        return f"{self.title} by {self.author}"

class Patron:
    def __init__(self, name, patron_id):
        self.name = name
        self.patron_id = patron_id
        self.checked_out_books = []

    def __str__(self):
        return self.name

class Library:
    def __init__(self):
        self.books = []
        self.patrons = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added book: {book}")

    def add_patron(self, patron):
        self.patrons.append(patron)
        print(f"Added patron: {patron}")

    def check_out(self, patron, book):
        if book not in self.books:
            print(f"Book {book} is not in the library's collection.")
            return
        
        if patron not in self.patrons:
            print(f"Patron {patron} is not registered in the library.")
            return

        if not book.checked_out:
            book.checked_out = True
            patron.checked_out_books.append(book)
            print(f"{book} checked out to {patron}.")
        else:
            print(f"{book} is already checked out.")

    def check_in(self, patron, book):
        if book not in self.books:
            print(f"Book {book} is not in the library's collection.")
            return
        
        if patron not in self.patrons:
            print(f"Patron {patron} is not registered in the library.")
            return

        if book in patron.checked_out_books:
            book.checked_out = False
            patron.checked_out_books.remove(book)
            print(f"{book} checked in by {patron}.")
        else:
            print(f"{patron} does not have {book} checked out.")

    def list_checked_out_books(self, patron):
        if patron not in self.patrons:
            print(f"Patron {patron} is not registered in the library.")
            return

        if patron.checked_out_books:
            print(f"Books checked out by {patron}:")
            for book in patron.checked_out_books:
                print(book)
        else:
            print(f"{patron} has no books checked out.")

# GUI Setup
import tkinter as tk
from tkinter import messagebox, simpledialog

class LibraryGUI:
    def __init__(self, root):
        self.library = Library()
        self.root = root
        self.root.title("Library Management System")

        # Setup GUI components
        self.create_widgets()

    def create_widgets(self):
        # Buttons and Labels
        tk.Button(self.root, text="Add Book", command=self.add_book).pack(pady=5)
        tk.Button(self.root, text="Add Patron", command=self.add_patron).pack(pady=5)
        tk.Button(self.root, text="Check Out Book", command=self.check_out_book).pack(pady=5)
        tk.Button(self.root, text="Check In Book", command=self.check_in_book).pack(pady=5)
        tk.Button(self.root, text="List Checked Out Books", command=self.list_checked_out_books).pack(pady=5)

    def add_book(self):
        title = simpledialog.askstring("Input", "Enter book title:")
        author = simpledialog.askstring("Input", "Enter book author:")
        isbn = simpledialog.askstring("Input", "Enter book ISBN:")
        if title and author and isbn:
            book = Book(title, author, isbn)
            self.library.add_book(book)
            messagebox.showinfo("Info", f"Added book: {book}")

    def add_patron(self):
        name = simpledialog.askstring("Input", "Enter patron name:")
        patron_id = simpledialog.askstring("Input", "Enter patron ID:")
        if name and patron_id:
            patron = Patron(name, patron_id)
            self.library.add_patron(patron)
            messagebox.showinfo("Info", f"Added patron: {patron}")

    def check_out_book(self):
        patron_name = simpledialog.askstring("Input", "Enter patron name:")
        book_title = simpledialog.askstring("Input", "Enter book title:")
        patron = next((p for p in self.library.patrons if p.name == patron_name), None)
        book = next((b for b in self.library.books if b.title == book_title), None)
        if patron and book:
            self.library.check_out(patron, book)
            messagebox.showinfo("Info", f"Checked out {book} to {patron}")
        else:
            messagebox.showwarning("Warning", "Patron or Book not found")

    def check_in_book(self):
        patron_name = simpledialog.askstring("Input", "Enter patron name:")
        book_title = simpledialog.askstring("Input", "Enter book title:")
        patron = next((p for p in self.library.patrons if p.name == patron_name), None)
        book = next((b for b in self.library.books if b.title == book_title), None)
        if patron and book:
            self.library.check_in(patron, book)
            messagebox.showinfo("Info", f"Checked in {book} from {patron}")
        else:
            messagebox.showwarning("Warning", "Patron or Book not found")

    def list_checked_out_books(self):
        patron_name = simpledialog.askstring("Input", "Enter patron name:")
        patron = next((p for p in self.library.patrons if p.name == patron_name), None)
        if patron:
            checked_out_books = "\n".join(str(book) for book in patron.checked_out_books)
            if checked_out_books:
                messagebox.showinfo("Checked Out Books", f"Books checked out by {patron}:\n{checked_out_books}")
            else:
                messagebox.showinfo("Checked Out Books", f"{patron} has no books checked out.")
        else:
            messagebox.showwarning("Warning", "Patron not found")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
