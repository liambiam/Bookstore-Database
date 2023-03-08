#=== Imports ===#

import sqlite3
from tabulate import tabulate

#=== Functions ===#

def addbook():

    print("\nAdd a book\n") 

    while True:

        # User input
        # Ensuring integer entered
        while True:
            try:
                new_id = int(input('Book ID: '))
                break
            except ValueError:
                print('Please enter an integer')

        new_title = input('Book Title: ')
        new_author = input('Book Author: ')
        
        while True:
            try:
                new_quantity = int(input('Book Quantity: '))
                break
            except ValueError:
                print('Please enter an integer')
        
        # Show user what they entere
        book = (new_id, new_title, new_author, new_quantity)
        table.append(book)
        print('You entered:\n')
        print(tabulate(table))
        print('''\nWould you like to add this to the database?
        y - yes
        n - no, re-enter data
        e - no, back to main menu
        ''')


        user_choice = input(': ').lower()

        # Add to database
        if user_choice == 'y':
            cursor.execute('''INSERT INTO books(
                id,Title,Author,Quantity) VALUES 
                (?,?,?,?)''', (new_id, new_title, new_author, new_quantity))
            db.commit()

        #Menu choice    
            print ('''New book data entered successfully.
            
            What would you like to do?
            e - enter a new book 
            r - return to the main menu
            ''')
            user_choice2 = input(': ').lower()
            if user_choice2 == 'e':
                pass
            else:
                break

        elif user_choice == 'n':
            pass
        else:
            break


def updatebook():

    print("\nUpdate a book\n")

    while True:
            
        while True:
            try:
                id = int(input('Book ID: ')) 
                break
            except ValueError:
                print('Please enter an integer')

        # Grab data based on ID entered
        book = cursor.execute('''SELECT * FROM books WHERE id = ?''', (id,))

        exist = cursor.fetchone()

        # Show if no data exists, mennu choice
        if exist is None:
            print('''No book exists with that ID exists. Would you like to...
            t - try again
            e - exit to main menu
            ''')
            user_choice2 = input(': ').lower()
            if user_choice2 == 't':
                pass
            else:
                break

        # If it exists show book, ask what they want to update 
        else:
            print('Here is the book:')
            book = cursor.execute('''SELECT * FROM books WHERE id = ?''', (id,))
            for row in book:
                    table.append(row)
            print(tabulate(table))


            print('''
            What would you like to update?
            i - ID
            t - Title
            a - Author
            q - Quantity
            ''')

            while True:

            # Update database based on user input
                user_choice = input(': ').lower()
                
                if user_choice == 'i':
                    while True:
                        try:
                            update_id = input('New ID: ')
                            break
                        except ValueError:
                            print('Please enter an integer')
                    cursor.execute('''UPDATE books SET id = ? WHERE id = ?''', (update_id,id,))        
                    print('Book updated')
                    break

                elif user_choice == 't':
                    update_title = input('New Title: ')
                    cursor.execute('''UPDATE books SET Title = ? WHERE id = ?''', (update_title,id,))
                    print('Book updated')
                    break

                elif user_choice == 'a':
                    update_author = input('New Author: ')
                    cursor.execute('''UPDATE books SET Author = ? WHERE id = ?''', (update_author,id,))
                    print('Book updated')
                    break

                elif user_choice == 'q':                       
                    while True:
                        try:
                            update_quantity = int(input('New Quantity: '))
                            break 
                        except ValueError:
                            print('Please enter an integer')
                    cursor.execute('''UPDATE books SET Quantity = ? WHERE id = ?''', (update_quantity,id,))
                    print('Book updated')
                    break

                else:
                    print('Incorrect choice')
                    break
            
            db.commit()

            # Show updated book, menu choices
            book = cursor.execute('''SELECT * FROM books WHERE id = ?''', (id,))
            for row in book:
                    table.append(row)
            print(tabulate(table))

            print ('''                
                What would you like to do?
                e - edit a new book 
                r - return to the main menu?
                ''')
            
            user_choice2 = input().lower()
            if user_choice2 == 'e':
                pass
            else:
                break


def deletebook():
    print("\nDelete a book\n")
    while True:

        # Making sure they want to continue
        user_choice = input('''Would you like to...
    c - continue
    b - back to main menu
    : ''')
        
        if user_choice == 'c':
            
            # Grabbing book if it exists
            id = input('Book ID: ')
            book = cursor.execute('''SELECT * FROM books WHERE id = ?''', (id,))
            exist = cursor.fetchone()

            # If not, ask them for their next choice 
            if exist is None:
                print('''No book exists with that ID exists. Would you like to...
                t - try again
                e - exit to main menu
                ''')
                user_choice2 = input(': ').lower()
                if user_choice2 == 't':
                    pass
                else:
                    break
            
            # If yes, display book, confirm deletion
            else:
                print('Here is the book:')
                book = cursor.execute('''SELECT * FROM books WHERE id = ?''', (id,))
                for row in book:
                    table.append(row)
                print(tabulate(table))
                
                user_choice3 = input('''Happy to delete?
                y - yes please
                n - no, back to delete menu
                : ''').lower()
                    
                if user_choice3 == 'y':
                    cursor.execute('''DELETE FROM books WHERE id = ? ''', (id,))
                    print('Book deleted')
                    db.commit()
                else:
                    pass
        else:
            break

def searchbook():
    print("\nSearch books\n")
    while True:

        # Search and display based on user input. Use 'like' to display books similar to input
        search_book = input('Enter the ID, Title, Author, or Quantity of the book: ')
        search_book = f'%{search_book}%'

        print('\nHere are the books with that data:\n')

        data = cursor.execute('''SELECT * FROM books WHERE id LIKE ? OR Title LIKE ? OR Author LIKE ? OR Quantity LIKE ?''',(search_book,search_book,search_book,search_book))
        
        for row in data:
            table.append(row)
        print(tabulate(table))                     

        user_choice = input('''Would you like to...
    s - search again
    b - back to main menu
    : ''')
        
        if user_choice == 's':
            pass
        else:
            break
        

def exitprogram():

    print('Database closed. Bye bye')
    db.close()


#=== Loading up the database ===#

        # Connect to database db
db = sqlite3.connect('ebookstore')

        # Get a cursor object
cursor = db.cursor() 

        # Create table if does not exist

cursor.execute('''
CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, Title TEXT,
Author TEXT, Quantity INTEGER)
''')

db.commit()

        # Insert rows, ignore if already exist
book_data = [
    (3001,'A Tale of Two Cities','Charles Dickens',30),
    (3002,'Harry Potter and the Philosopher\'s Stone','J.K. Rowling',40),
    (3003,'The Lion, the Witch and the Wardrobe','C. S. Lewis',25),
    (3004,'The Lord of the Rings','J.R.R Tolkien',37),
    (3005,'Alice in Wonderland','Lewis Carroll',12)
    ] 

cursor.executemany('''INSERT or IGNORE INTO books(id, Title, Author, Quantity) VALUES(?,?,?,?)''',
    book_data)

db.commit()

        # Base table for data display   
table = [('ID', 'Title', 'Author', 'Quantity'), ()]



#=== USER MENU ===#


        # Menu options

while True:

    print('''
    **eBook Database Main Menu**

    What would you like to do?

    a - add a new book
    u - update a book
    d - delete a book
    s - search for a book
    e - exit the database
    ''')

        # Call functions dependent on user choice

    clerk_choice = input('Your choice: ').lower()

    if clerk_choice == 'a':
        addbook()        
    elif clerk_choice == 'u':
        updatebook()
    elif clerk_choice == 'd':
        deletebook()
    elif clerk_choice == 's':
        searchbook()
    elif clerk_choice == 'e':
        exitprogram()
        break
    else:
        print('Incorrect choice, try again')
