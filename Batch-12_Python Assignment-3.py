import sys

# Custom exceptions for validation rules
class DuplicateError(Exception):
    pass

class ValidationError(Exception):
    pass


# 1. Person (Parent Class)
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Name : {self.name}")
        print(f"Age : {self.age}")


# 2. Member (Child of Person)
class Member(Person):
    def __init__(self, name, age, member_id):
        super().__init__(name, age)
        self.member_id = member_id
        self.borrowed_books = []  # Stores Book objects

    # Method Overriding
    def display_info(self):
        print(f"Member ID : {self.member_id}")
        super().display_info()
        print(f"Borrowed Books : {len(self.borrowed_books)}")

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)


# 3. Book
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        # Encapsulation: private attribute with double underscore
        self.__available = True 

    # Getter property
    @property
    def available(self):
        return self.__available

    # Setter property
    @available.setter
    def available(self, status):
        if isinstance(status, bool):
            self.__available = status

    def display_book(self):
        print(f"ISBN : {self.isbn}")
        print(f"Title : {self.title}")
        print(f"Author : {self.author}")
        status_str = "Available" if self.available else "Borrowed"
        print(f"Status : {status_str}")


# 4. Library (Uses Composition)
class Library:
    def __init__(self):
        # Composition: Library contains and manages Book and Member instances
        self.books = {}    # Key: ISBN, Value: Book object
        self.members = {}  # Key: Member ID, Value: Member object

    def add_book(self, title, author, isbn):
        if not title.strip() or not author.strip() or not isbn.strip():
            raise ValidationError("Title, Author, and ISBN cannot be empty.")
        if isbn in self.books:
            raise DuplicateError("ISBN already exists.")
        
        # Creating Book instance inside the Library container
        self.books[isbn] = Book(title, author, isbn)
        print("Book added successfully!")

    def register_member(self, name, age, member_id):
        if not name.strip() or not member_id.strip():
            raise ValidationError("Name and Member ID cannot be empty.")
        if age <= 0:
            raise ValidationError("Age must be greater than 0.")
        if member_id in self.members:
            raise DuplicateError("Member ID already exists.")

        # Creating Member instance inside the Library container
        self.members[member_id] = Member(name, age, member_id)
        print("Member registered successfully!")

    def borrow_book(self, member_id, isbn):
        if member_id not in self.members:
            raise ValidationError("Member not found.")
        if isbn not in self.books:
            raise ValidationError("Book not found.")

        member = self.members[member_id]
        book = self.books[isbn]

        if not book.available:
            print("Sorry! This book is currently unavailable.")
            return

        if book in member.borrowed_books:
            raise ValidationError("A member cannot borrow the same book twice.")

        book.available = False
        member.borrow = member.borrow_book(book)
        print("Book borrowed successfully.")

    def return_book(self, member_id, isbn):
        if member_id not in self.members:
            raise ValidationError("Member not found.")
        if isbn not in self.books:
            raise ValidationError("Book not found.")

        member = self.members[member_id]
        book = self.books[isbn]

        if book not in member.borrowed_books:
            raise ValidationError("This member hasn't borrowed this book.")

        book.available = True
        member.return_book(book)
        print("Book returned successfully.")

    def show_books(self):
        if not self.books:
            print("No books available in the library.")
            return
        print("------------- BOOK LIST -------------")
        for book in self.books.values():
            book.display_book()
            print("-------------------------------------")

    def show_members(self):
        if not self.members:
            print("No registered members.")
            return
        print("----------- MEMBER LIST ------------")
        for member in self.members.values():
            member.display_info()
            print("------------------------------------")

    def search_book(self, title):
        if not title.strip():
            raise ValidationError("Search title cannot be empty.")
        
        found = False
        # Case-insensitive partial matching
        for book in self.books.values():
            if title.lower() == book.title.lower():
                if not found:
                    print("Book Found!")
                    found = True
                book.display_book()
        
        if not found:
            print("Book not found.")


# Helper to handle uniform pause behavior
def pause():
    input("Press Enter to continue...")


# User Interface Execution Loop
def main():
    library = Library()

    while True:
        print("=========================================")
        print("LIBRARY MANAGEMENT SYSTEM")
        print("=========================================")
        print("1. Add Book")
        print("2. Register Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Show All Books")
        print("6. Show All Members")
        print("7. Search Book")
        print("8. Exit")
        
        try:
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                print("----- Add New Book -----")
                title = input("Enter Book Title : ")
                author = input("Enter Author : ")
                isbn = input("Enter ISBN : ")
                library.add_book(title, author, isbn)
                pause()

            elif choice == '2':
                print("----- Register Member -----")
                member_id = input("Enter Member ID : ")
                name = input("Enter Name : ")
                age_input = input("Enter Age : ")
                
                if not age_input.strip():
                    raise ValidationError("Age cannot be empty.")
                try:
                    age = int(age_input)
                except ValueError:
                    raise ValidationError("Age must be a valid integer number.")
                    
                library.register_member(name, age, member_id)
                pause()

            elif choice == '3':
                print("------ Borrow Book ------")
                member_id = input("Enter Member ID : ")
                isbn = input("Enter Book ISBN : ")
                library.borrow_book(member_id, isbn)
                pause()

            elif choice == '4':
                print("------ Return Book ------")
                member_id = input("Enter Member ID : ")
                isbn = input("Enter Book ISBN : ")
                library.return_book(member_id, isbn)
                pause()

            elif choice == '5':
                library.show_books()
                pause()

            elif choice == '6':
                library.show_members()
                pause()

            elif choice == '7':
                print("------ Search Book ------")
                title = input("Enter Book Title : ")
                library.search_book(title)
                pause()

            elif choice == '8':
                print("Thank you for using Library Management System.")
                print("Goodbye!")
                sys.exit()

            else:
                print("Error: Invalid menu choice. Please select 1-8.")
                pause()

        except (DuplicateError, ValidationError) as err:
            print(f"Error: {err}")
            pause()
        except Exception as e:
            print(f"Unexpected Runtime Error: {e}")
            pause()

if __name__ == "__main__":
    main()