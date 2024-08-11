import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class Book:
    def __init__(self, title, author, genre, publication_year, rating=None, review=None):
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_year = publication_year
        self.rating = rating
        self.review = review

    def __str__(self):
        return (f"Title: {self.title}, Author: {self.author}, Genre: {self.genre}, "
                f"Year: {self.publication_year}, Rating: {self.rating}, Review: {self.review}")

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, title):
        book = self.search_book(title)
        if book:
            self.books.remove(book)
            return True
        return False

    def search_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def display_books(self, sort_by=None):
        if sort_by:
            if sort_by == 'title':
                sorted_books = sorted(self.books, key=lambda x: x.title.lower())
            elif sort_by == 'author':
                sorted_books = sorted(self.books, key=lambda x: x.author.lower())
            elif sort_by == 'genre':
                sorted_books = sorted(self.books, key=lambda x: x.genre.lower())
            else:
                sorted_books = self.books
        else:
            sorted_books = self.books

        return "\n".join(str(book) for book in sorted_books)

    def save_to_file(self, filename="library.csv"):
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Author", "Genre", "Publication Year", "Rating", "Review"])
                for book in self.books:
                    writer.writerow([book.title, book.author, book.genre, book.publication_year,
                                     book.rating if book.rating else '', book.review if book.review else ''])
        except IOError as e:
            print(f"Error saving to file: {e}")

    def load_from_file(self, filename="library.csv"):
        self.books = []
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    title, author, genre, publication_year, rating, review = row
                    book = Book(title, author, genre, int(publication_year),
                                float(rating) if rating else None, review)
                    self.books.append(book)
        except FileNotFoundError:
            print("File not found. Starting with an empty library.")
        except IOError as e:
            print(f"Error loading from file: {e}")

class LibraryGUI:
    def __init__(self, root):
        self.library = Library()
        self.root = root
        self.root.title("Library Management System")

        self.tab_control = ttk.Notebook(root)
        self.tab_library = ttk.Frame(self.tab_control)
        self.tab_rate_review = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_library, text='Library')
        self.tab_control.add(self.tab_rate_review, text='Rate & Review')
        self.tab_control.pack(expand=1, fill="both")

        self.create_library_tab()
        self.create_rate_review_tab()

    def create_library_tab(self):
        # Add Book
        self.label_title = ttk.Label(self.tab_library, text="Title:")
        self.label_title.grid(row=0, column=0, padx=10, pady=10)
        self.entry_title = ttk.Entry(self.tab_library)
        self.entry_title.grid(row=0, column=1, padx=10, pady=10)

        self.label_author = ttk.Label(self.tab_library, text="Author:")
        self.label_author.grid(row=1, column=0, padx=10, pady=10)
        self.entry_author = ttk.Entry(self.tab_library)
        self.entry_author.grid(row=1, column=1, padx=10, pady=10)

        self.label_genre = ttk.Label(self.tab_library, text="Genre:")
        self.label_genre.grid(row=2, column=0, padx=10, pady=10)
        self.entry_genre = ttk.Entry(self.tab_library)
        self.entry_genre.grid(row=2, column=1, padx=10, pady=10)

        self.label_year = ttk.Label(self.tab_library, text="Publication Year:")
        self.label_year.grid(row=3, column=0, padx=10, pady=10)
        self.entry_year = ttk.Entry(self.tab_library)
        self.entry_year.grid(row=3, column=1, padx=10, pady=10)

        self.label_rating = ttk.Label(self.tab_library, text="Rating:")
        self.label_rating.grid(row=4, column=0, padx=10, pady=10)
        self.entry_rating = ttk.Entry(self.tab_library)
        self.entry_rating.grid(row=4, column=1, padx=10, pady=10)

        self.label_review = ttk.Label(self.tab_library, text="Review:")
        self.label_review.grid(row=5, column=0, padx=10, pady=10)
        self.entry_review = ttk.Entry(self.tab_library)
        self.entry_review.grid(row=5, column=1, padx=10, pady=10)

        self.button_add = ttk.Button(self.tab_library, text="Add Book", command=self.add_book)
        self.button_add.grid(row=6, column=0, padx=10, pady=10)

        self.button_remove = ttk.Button(self.tab_library, text="Remove Book", command=self.remove_book)
        self.button_remove.grid(row=6, column=1, padx=10, pady=10)

        self.button_save = ttk.Button(self.tab_library, text="Save Library", command=self.save_library)
        self.button_save.grid(row=7, column=0, padx=10, pady=10)

        self.button_load = ttk.Button(self.tab_library, text="Load Library", command=self.load_library)
        self.button_load.grid(row=7, column=1, padx=10, pady=10)

        self.button_sort_title = ttk.Button(self.tab_library, text="Sort by Title", command=lambda: self.sort_books('title'))
        self.button_sort_title.grid(row=8, column=0, padx=10, pady=10)

        self.button_sort_author = ttk.Button(self.tab_library, text="Sort by Author", command=lambda: self.sort_books('author'))
        self.button_sort_author.grid(row=8, column=1, padx=10, pady=10)

        self.button_sort_genre = ttk.Button(self.tab_library, text="Sort by Genre", command=lambda: self.sort_books('genre'))
        self.button_sort_genre.grid(row=9, column=0, padx=10, pady=10)

        self.text_display = tk.Text(self.tab_library, height=15, width=60)
        self.text_display.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    def create_rate_review_tab(self):
        self.label_rate_title = ttk.Label(self.tab_rate_review, text="Book Title:")
        self.label_rate_title.grid(row=0, column=0, padx=10, pady=10)
        self.entry_rate_title = ttk.Entry(self.tab_rate_review)
        self.entry_rate_title.grid(row=0, column=1, padx=10, pady=10)

        self.label_rate_rating = ttk.Label(self.tab_rate_review, text="Rating:")
        self.label_rate_rating.grid(row=1, column=0, padx=10, pady=10)
        self.entry_rate_rating = ttk.Entry(self.tab_rate_review)
        self.entry_rate_rating.grid(row=1, column=1, padx=10, pady=10)

        self.label_rate_review = ttk.Label(self.tab_rate_review, text="Review:")
        self.label_rate_review.grid(row=2, column=0, padx=10, pady=10)
        self.entry_rate_review = ttk.Entry(self.tab_rate_review)
        self.entry_rate_review.grid(row=2, column=1, padx=10, pady=10)

        self.button_rate = ttk.Button(self.tab_rate_review, text="Submit Rating & Review", command=self.submit_rating_review)
        self.button_rate.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def add_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        genre = self.entry_genre.get()
        year = self.entry_year.get()
        rating = self.entry_rating.get()
        review = self.entry_review.get()

        if not (title and author and genre and year):
            messagebox.showwarning("Input Error", "All fields except rating and review are required.")
            return

        try:
            year = int(year)
            rating = float(rating) if rating else None
        except ValueError:
            messagebox.showwarning("Input Error", "Publication Year must be an integer and Rating must be a float.")
            return

        book = Book(title, author, genre, year, rating, review)
        self.library.add_book(book)
        self.display_books()
        self.clear_entries()

    def remove_book(self):
        title = self.entry_title.get()
        if self.library.remove_book(title):
            self.display_books()
            self.clear_entries()
        else:
            messagebox.showwarning("Book Not Found", f"No book with title '{title}' found.")

    def submit_rating_review(self):
        title = self.entry_rate_title.get()
        rating = self.entry_rate_rating.get()
        review = self.entry_rate_review.get()

        if not title:
            messagebox.showwarning("Input Error", "Book title is required.")
            return

        book = self.library.search_book(title)
        if book:
            try:
                book.rating = float(rating) if rating else None
                book.review = review
                self.display_books()
                self.clear_rate_review_entries()
                messagebox.showinfo("Success", "Rating and review updated.")
            except ValueError:
                messagebox.showwarning("Input Error", "Rating must be a float.")
        else:
            messagebox.showwarning("Book Not Found", f"No book with title '{title}' found.")

    def sort_books(self, criteria):
        self.display_books(sort_by=criteria)

    def display_books(self, sort_by=None):
        self.text_display.delete(1.0, tk.END)
        books_info = self.library.display_books(sort_by=sort_by)
        self.text_display.insert(tk.END, books_info)

    def save_library(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            self.library.save_to_file(filename)
            messagebox.showinfo("Success", f"Library data saved to {filename}")

    def load_library(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.library.load_from_file(filename)
            self.display_books()
            messagebox.showinfo("Success", f"Library data loaded from {filename}")

    def clear_entries(self):
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)
        self.entry_review.delete(0, tk.END)

    def clear_rate_review_entries(self):
        self.entry_rate_title.delete(0, tk.END)
        self.entry_rate_rating.delete(0, tk.END)
        self.entry_rate_review.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
