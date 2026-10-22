# This code defines a class named book, I need to create a function that check if the book is a "unique" one,
# the definition for unique is the the particular book was purchased by one or more person but only.
# if the book was purchased by a person and this person purchased another book, then the book that was candidate for being "unique" is no longer a unique
# the function need to 

class book:
    def __init__(self, purchase_by, book_name):
        self.purchase_by = purchase_by
        self.book_name = book_name

    def __str__(self):
        return f"{self.book_name} purchased by {self.purchase_by}"
    
if __name__ == "__main__":
    book1 = book("Alice", "The Great Gatsby")
    book1 = book("Alice", "The King Jo)
    book1 = book("Alice", "The Great Gatsby")
    book1 = book("Alice", "The Great Gatsby")
    print(book1)