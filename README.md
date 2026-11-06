# Library Book Recommendation System

This is a simple Python project that helps users find books based on their favourite genre. Users can search for books, get recommendations and add new books.

## Features

- View all books in the database.
- Search by book title, author or genre.
- Get recommendations by selecting a genre.
- Add new books and save them in the database.

## Tools Used

- Python
- Tkinter for the application window
- SQLite3 for storing book details

## Project Files

```text
Library_Book_Recommendation_Project/
├── app.py
├── library.db
└── README.md
```

`app.py` contains the program, `library.db` stores the book details, and this README provides project information.

## How to Run

1. Install Python.
2. Open the project folder in Visual Studio Code.
3. Open the terminal and run:

   ```bash
   python app.py
   ```

4. The application window will open.

Keep `app.py` and `library.db` in the same folder.

## How to Use

- Click **Show All** to view all books.
- Enter a title, author or genre and click **Search** to find a book.
- Select a genre and click **Recommend Books** to see matching books.
- Enter a title, author and genre in the Add a New Book section, then click **Add Book**.

## Database

The SQLite database contains a table named `books` with these columns:

| Column | Description |
|---|---|
| id | Unique ID of the book |
| title | Book title |
| author | Author name |
| genre | Book category |
| description | Short book description |

## Recommendation Method

The program recommends books by matching the genre selected by the user with the genres stored in the database. This is a basic genre-based system and does not use machine learning.

## Conclusion

This project helped me practise Python, create a GUI with Tkinter and store and search book details using SQLite3.

## Team Members 
Priyani Ghosh (Team Leader)

Shama Parveen 

Prodyut Dey 

Md Khushtar Nawaz
