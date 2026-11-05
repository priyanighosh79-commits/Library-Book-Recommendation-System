import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from pathlib import Path

DATABASE_FILE = Path(__file__).with_name("library.db")


def connect_database():
    """Open a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_FILE)


def create_table():
    """Create the books table and add sample books the first time the app runs."""
    with connect_database() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                description TEXT
            )
        """)

        cursor.execute("SELECT COUNT(*) FROM books")
        book_count = cursor.fetchone()[0]

        if book_count == 0:
            sample_books = [
                ("The Hobbit", "J.R.R. Tolkien", "Fantasy",
                 "A hobbit goes on an unexpected adventure."),
                ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "Fantasy",
                 "A young wizard discovers the magical world."),
                ("The Alchemist", "Paulo Coelho", "Adventure",
                 "A shepherd travels in search of his dream."),
                ("Around the World in Eighty Days", "Jules Verne", "Adventure",
                 "A journey around the world against the clock."),
                ("Pride and Prejudice", "Jane Austen", "Romance",
                 "A classic story about love and misunderstandings."),
                ("The Fault in Our Stars", "John Green", "Romance",
                 "Two teenagers meet and form a close bond."),
                ("A Brief History of Time", "Stephen Hawking", "Science",
                 "An introduction to space, time and the universe."),
                ("The Selfish Gene", "Richard Dawkins", "Science",
                 "An accessible introduction to evolutionary biology."),
                ("The Blue Umbrella", "Ruskin Bond", "Fiction",
                 "A simple story set in a Himalayan village."),
                ("The Guide", "R. K. Narayan", "Fiction",
                 "A novel about a tour guide and his changing life.")
            ]
            cursor.executemany("""
                INSERT INTO books (title, author, genre, description)
                VALUES (?, ?, ?, ?)
            """, sample_books)


class BookRecommendationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Book Recommendation System")
        self.root.geometry("1050x720")
        self.root.minsize(850, 650)

        self.create_widgets()
        self.show_all_books()

    def create_widgets(self):
        heading = ttk.Label(
            self.root,
            text="Library Book Recommendation System",
            font=("Arial", 18, "bold")
        )
        heading.pack(pady=(10, 3))

        intro = ttk.Label(
            self.root,
            text="Search for books, choose a genre, or add a new book."
        )
        intro.pack(pady=(0, 7))

        search_frame = ttk.LabelFrame(self.root, text="Search Books")
        search_frame.pack(fill="x", padx=12, pady=4)

        ttk.Label(search_frame, text="Title, author or genre:").grid(
            row=0, column=0, padx=7, pady=7, sticky="w"
        )

        self.search_entry = ttk.Entry(search_frame, width=35)
        self.search_entry.grid(row=0, column=1, padx=7, pady=7)

        ttk.Button(
            search_frame, text="Search", command=self.search_books
        ).grid(row=0, column=2, padx=5, pady=7)

        ttk.Button(
            search_frame, text="Show All", command=self.show_all_books
        ).grid(row=0, column=3, padx=5, pady=7)

        recommend_frame = ttk.LabelFrame(self.root, text="Get Recommendations")
        recommend_frame.pack(fill="x", padx=12, pady=4)

        ttk.Label(recommend_frame, text="Choose your favourite genre:").grid(
            row=0, column=0, padx=7, pady=7, sticky="w"
        )

        self.genre_box = ttk.Combobox(
            recommend_frame,
            values=["Fantasy", "Adventure", "Romance", "Science", "Fiction"],
            state="readonly",
            width=22
        )
        self.genre_box.grid(row=0, column=1, padx=7, pady=7)
        self.genre_box.set("Fantasy")

        ttk.Button(
            recommend_frame,
            text="Recommend Books",
            command=self.recommend_books
        ).grid(row=0, column=2, padx=7, pady=7)

        add_frame = ttk.LabelFrame(self.root, text="Add a New Book")
        add_frame.pack(fill="x", padx=12, pady=4)

        ttk.Label(add_frame, text="Title:").grid(row=0, column=0, padx=5, pady=8)
        self.title_entry = ttk.Entry(add_frame, width=22)
        self.title_entry.grid(row=0, column=1, padx=5, pady=8)

        ttk.Label(add_frame, text="Author:").grid(row=0, column=2, padx=5, pady=8)
        self.author_entry = ttk.Entry(add_frame, width=20)
        self.author_entry.grid(row=0, column=3, padx=5, pady=8)

        ttk.Label(add_frame, text="Genre:").grid(row=0, column=4, padx=5, pady=8)
        self.new_genre_entry = ttk.Entry(add_frame, width=15)
        self.new_genre_entry.grid(row=0, column=5, padx=5, pady=8)

        ttk.Button(
            add_frame, text="Add Book", command=self.add_book
        ).grid(row=0, column=6, padx=8, pady=8)


        list_frame = ttk.LabelFrame(self.root, text="Book Collection")
        list_frame.pack(fill="both", expand=True, padx=12, pady=4)

        columns = ("id", "title", "author", "genre")
        self.book_table = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=8
        )
        self.book_table.heading("id", text="ID")
        self.book_table.heading("title", text="Book Title")
        self.book_table.heading("author", text="Author")
        self.book_table.heading("genre", text="Genre")

        self.book_table.column("id", width=45, anchor="center")
        self.book_table.column("title", width=330)
        self.book_table.column("author", width=220)
        self.book_table.column("genre", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.book_table.yview
        )
        self.book_table.configure(yscrollcommand=scrollbar.set)

        self.book_table.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=5)

        self.status_label = ttk.Label(self.root, text="Ready", anchor="w")
        self.status_label.pack(fill="x", padx=15, pady=(1, 6))

    def display_books(self, books):
        """Remove old rows and display the books returned by a query."""
        for row in self.book_table.get_children():
            self.book_table.delete(row)

        for book in books:
            self.book_table.insert("", "end", values=book)

        self.status_label.config(text=f"{len(books)} book(s) displayed.")

    def show_all_books(self):
        with connect_database() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, title, author, genre
                FROM books
                ORDER BY title
            """)
            books = cursor.fetchall()

        self.display_books(books)

    def search_books(self):
        search_text = self.search_entry.get().strip()

        if not search_text:
            messagebox.showinfo("Search", "Please enter a title, author or genre.")
            return

        search_pattern = f"%{search_text}%"

        with connect_database() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, title, author, genre
                FROM books
                WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?
                ORDER BY title
            """, (search_pattern, search_pattern, search_pattern))
            books = cursor.fetchall()

        self.display_books(books)

        if not books:
            messagebox.showinfo("Search Result", "No matching books were found.")

    def recommend_books(self):
        selected_genre = self.genre_box.get()

        with connect_database() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, title, author, genre
                FROM books
                WHERE genre = ? COLLATE NOCASE
                ORDER BY title
            """, (selected_genre,))
            books = cursor.fetchall()

        self.display_books(books)

        if books:
            messagebox.showinfo(
                "Recommendations",
                f"Here are {len(books)} book(s) in the {selected_genre} genre."
            )
        else:
            messagebox.showinfo(
                "Recommendations",
                "No books found in this genre. You can add one below."
            )

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.new_genre_entry.get().strip()

        if not title or not author or not genre:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the title, author and genre."
            )
            return

        with connect_database() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO books (title, author, genre, description)
                VALUES (?, ?, ?, ?)
            """, (title, author, genre, "Added by the user."))

        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.new_genre_entry.delete(0, tk.END)

        self.show_all_books()
        messagebox.showinfo("Success", "The book was added successfully.")


if __name__ == "__main__":
    create_table()

    main_window = tk.Tk()
    app = BookRecommendationApp(main_window)
    main_window.mainloop()
