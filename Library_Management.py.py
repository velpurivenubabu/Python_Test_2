from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, isbn, genre, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.quantity = quantity
    
    def display_info(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"ISBN: {self.isbn}")
        print(f"Genre: {self.genre}")
        print(f"Quantity: {self.quantity}")
        print("----------------------")


class Borrower:
    def __init__(self, name, contact_details, membership_id):
        self.name = name
        self.contact_details = contact_details
        self.membership_id = membership_id
    
    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Contact Details: {self.contact_details}")
        print(f"Membership ID: {self.membership_id}")
        print("----------------------")


class Library:
    def __init__(self):
        self.books = []
        self.borrowers = []
        self.borrowed_books = {}  # {isbn: [(membership_id, due_date), ...]}
    
    # Book Management
    def add_book(self, title, author, isbn, genre, quantity):
        new_book = Book(title, author, isbn, genre, quantity)
        self.books.append(new_book)
        print(f"Book '{title}' added to the library.")
    
    def update_book(self, isbn, new_title=None, new_author=None, new_quantity=None):
        for book in self.books:
            if book.isbn == isbn:
                if new_title:
                    book.title = new_title
                if new_author:
                    book.author = new_author
                if new_quantity is not None:
                    book.quantity = new_quantity
                print(f"Book with ISBN {isbn} updated.")
                return
        print(f"Book with ISBN {isbn} not found.")
    
    def remove_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                print(f"Book with ISBN {isbn} removed from the library.")
                return
        print(f"Book with ISBN {isbn} not found.")
    
    # Borrower Management
    def add_borrower(self, name, contact_details, membership_id):
        new_borrower = Borrower(name, contact_details, membership_id)
        self.borrowers.append(new_borrower)
        print(f"Borrower '{name}' added to the library system.")
    
    def update_borrower(self, membership_id, new_name=None, new_contact_details=None):
        for borrower in self.borrowers:
            if borrower.membership_id == membership_id:
                if new_name:
                    borrower.name = new_name
                if new_contact_details:
                    borrower.contact_details = new_contact_details
                print(f"Borrower with membership ID {membership_id} updated.")
                return
        print(f"Borrower with membership ID {membership_id} not found.")
    
    def remove_borrower(self, membership_id):
        for borrower in self.borrowers:
            if borrower.membership_id == membership_id:
                self.borrowers.remove(borrower)
                print(f"Borrower with membership ID {membership_id} removed from the library system.")
                # Remove borrowed books by this borrower
                self.remove_borrowed_books(membership_id)
                return
        print(f"Borrower with membership ID {membership_id} not found.")
    
    def remove_borrowed_books(self, membership_id):
        # Remove all borrowed books associated with a borrower
        for isbn in list(self.borrowed_books):
            self.borrowed_books[isbn] = [(m_id, due_date) for m_id, due_date in self.borrowed_books[isbn] if m_id != membership_id]
            if not self.borrowed_books[isbn]:
                del self.borrowed_books[isbn]
    
    # Book Borrowing and Returning
    def borrow_book(self, membership_id, isbn):
        # Check if book exists and available
        for book in self.books:
            if book.isbn == isbn:
                if book.quantity > 0:
                    due_date = datetime.now() + timedelta(days=14)  # 2 weeks from now
                    if isbn in self.borrowed_books:
                        self.borrowed_books[isbn].append((membership_id, due_date))
                    else:
                        self.borrowed_books[isbn] = [(membership_id, due_date)]
                    book.quantity -= 1
                    print(f"Book with ISBN {isbn} borrowed by borrower with membership ID {membership_id}.")
                    print(f"Due Date: {due_date.strftime('%Y-%m-%d')}")
                    return True
                else:
                    print(f"Book with ISBN {isbn} is currently not available for borrowing.")
                    return False
        print(f"Book with ISBN {isbn} not found in the library.")
        return False
    
    def return_book(self, membership_id, isbn):
        if isbn in self.borrowed_books:
            for i, (m_id, due_date) in enumerate(self.borrowed_books[isbn]):
                if m_id == membership_id:
                    del self.borrowed_books[isbn][i]
                    for book in self.books:
                        if book.isbn == isbn:
                            book.quantity += 1
                            print(f"Book with ISBN {isbn} returned by borrower with membership ID {membership_id}.")
                            return True
        print(f"Book with ISBN {isbn} not found in borrowed records for borrower with membership ID {membership_id}.")
        return False
    
    # Book Search and Availability
    def search_book(self, query):
        found_books = []
        for book in self.books:
            if (query.lower() in book.title.lower() or
                query.lower() in book.author.lower() or
                query.lower() in book.genre.lower()):
                found_books.append(book)
        return found_books
    
    def display_available_books(self):
        for book in self.books:
            print(f"{book.title} - Available Quantity: {book.quantity}")

if __name__ == "__main__":
    library = Library()
    
    # Adding books
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", "Classic", 5)
    library.add_book("To Kill a Mockingbird", "Harper Lee", "9780061120084", "Fiction", 2)
    library.add_book("The Merchant", "J.Done", "9780061120666", "Classic", 8)
    library.add_book("The Elephant King ", "RS.Brown", "9780061120555", "Friction", 7)
    # Adding borrowers
    library.add_borrower("Bhavani", "bhavani@227gmail.com", "MEM001")
    library.add_borrower("Siva", "siva123@gmail.com", "MEM002")
    library.add_borrower("Ram", "ram225@gmail.com", "MEM003")
    library.add_borrower("Lavanya", "lavanya325@gmail.com", "MEM004")
    library.add_borrower("Gayatri", "gayatri@157gmail.com", "MEM005")
    # Borrowing books
    library.borrow_book("MEM001", "9780743273565")
    library.borrow_book("MEM002", "9780061120084")  
    library.borrow_book("MEM003", "9780061120666")
    library.borrow_book("MEM004", "9780061120555")
    library.borrow_book("MEM004", "9780061120084")
    library.borrow_book("MEM001", "9780061120084")  # Here I am Trying to borrow boock witch is out out stock so it returns the book is currently not available for borrowing.
    # Returning books
    library.return_book("MEM001", "9780743273565")
    library.return_book("MEM004", "9780061120084")
    # Displaying available books
    print("\nAvailable Books:")
    library.display_available_books()
    
    # Searching for books
    print("\nSearching for 'mockingbird':")
    search_results = library.search_book("mockingbird")
    for book in search_results:
        book.display_info()

    # Updating books
    library.update_book("9780061120084", "The Hunter","Venubabu",2)
    
    book.display_info() # Here I am getting the updated book list