''' A Python module which contains common functions that the book search, checkout,
    return and recommend modules use to interact with the database. It also contains
    the initialisation function which populates the database with data in the text files. '''

import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
import numpy as np
from datetime import datetime
from PIL import Image


def create_connection(db_file):
    """ create a database connection to SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def reset_database():
    ''' function for resetting database to initial values from text files '''
    
    initialise_library()
    
    filepathBook = "Book_Info.txt" 
    tablenameBook = "BookInfo"
    create_book_table("Library.db")
    
    filepathLoan = "Loan_History.txt" 
    tablenameLoan = "LoanHistory"
    create_loan_table("Library.db")

    get_file_data(filepathBook, tablenameBook)
    get_file_data(filepathLoan, tablenameLoan)
        

def initialise_library():
    '''function for creating BookInfo and LoanHistory table in database'''
    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS BookInfo(
                       ID INTEGER PRIMARY KEY, Genre TEXT, Title TEXT,
                       Author TEXT, LoanPeriod INTEGER,
                       PurchaseDate DATE, MemberID CHAR(4));''')
        conn.commit()
    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()

    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS LoanHistory(
                       TransactionID INTEGER PRIMARY KEY AUTOINCREMENT, BookID INTEGER, CheckoutDate DATE, ReturnDate DATE);''')
        conn.commit()
    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()

            

def create_book_table(db_file):
    ''' function for creating BookInfo table in database'''

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE BookInfo') 
        cursor.execute('''CREATE TABLE IF NOT EXISTS BookInfo(
                       ID INTEGER PRIMARY KEY, Genre TEXT, Title TEXT,
                       Author TEXT, LoanPeriod INTEGER,
                       PurchaseDate DATE, MemberID CHAR(4));''')
        conn.commit()
    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()


def create_loan_table(db_file):
    ''' function for creating LoanHistory table in database'''

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE LoanHistory') 
        cursor.execute('''CREATE TABLE IF NOT EXISTS LoanHistory(
                       TransactionID INTEGER PRIMARY KEY AUTOINCREMENT, BookID INTEGER, CheckoutDate DATE, ReturnDate DATE);''')
        conn.commit()
    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()
    
    
            
def get_file_data(filename, tablename):
    ''' function that reads from specified txt file in order to populate the
        corresponding table in db '''


    f = open(filename, "r")
    next(f)
    try:
        while True:
            line = f.readline()
            if line=="":
                break
            strip = line.strip("\n")
            record = strip.split(",")
            update_table(tablename, record)
    except Error as e:
        print (e)
    finally:
        if f:
            f.close()
    
        


def update_table(tablename, dataIn):
    ''' Function which inserts txt file data into corresponding table in db at
        their correct cell positions'''
    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        if tablename == "BookInfo":
            cursor.execute('INSERT INTO '+tablename+' VALUES (?, ?, ?, ?, ?, ?, ?)', (dataIn))
            conn.commit()
            
        else:
            cursor.execute('INSERT INTO '+tablename+' VALUES (?, ?, ?, ?)', (dataIn))
            conn.commit()
            
    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()
            
            
            
def dbcheckout_book(memberId, bookId):
    ''' function for checking out books once all criteria has been met'''

    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()

        if book_available(bookId):
            # update "BookInfo" table with member's ID for their chosen book
            cursor.execute('UPDATE BookInfo SET MemberID=? WHERE ID=?', (memberId, bookId))

            # insert new transaction once book has been checked out
            cursor.execute('INSERT INTO LoanHistory (BookId, CheckoutDate, ReturnDate) VALUES (?, ?, null)', (bookId, datetime.today().strftime('%Y-%m-%d')))
            conn.commit()
        else:
            print("Book currently being borrowed, so unavailable to checkout")
            
        #checkout complete!!
    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()

def get_book_data(bookId):
    ''' function which simply reads all book information for a given Book ID
        returns all elements of book info record as a list'''

    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        
        # get book info according to book ID provided
        cursor.execute('SELECT * FROM BookInfo WHERE ID=?', (bookId, ))
        book = cursor.fetchall()[0]
        return book
        
        conn.commit()
        
    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()
            
            
def dbreturn_book(bookId):
    ''' function for returning books once all criteria has been met'''

    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        
        # update "LoanHistory" table with return date for selected book to today's date
        cursor.execute('UPDATE LoanHistory SET ReturnDate=? WHERE TransactionID=(SELECT MAX(TransactionID) FROM LoanHistory WHERE BookID=?)', (datetime.today().strftime('%Y-%m-%d'), bookId))
        
        # update "BookInfo" table removing the memberID as book is now available once returned
        cursor.execute('UPDATE BookInfo SET MemberID=0 WHERE ID=?', (bookId, ))
        conn.commit()

        #return complete!!
    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()


def book_available(bookId):
    ''' function for checking if book is available given Book ID
        returns True if book is available
        returns False if book is unavailable '''

    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        
        # get member holding selected book
        cursor.execute('SELECT MemberID FROM BookInfo WHERE ID=?', (bookId, ))
        
        member = str(cursor.fetchall())
        member = member.strip("[(',)]")
        
        conn.commit()
        if member == '0':
            return True
            conn.close()
        else:
            return False
            conn.close()
        
    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()
            
            
def currently_holding(memberId):
    ''' function checking who is borrowing a book, given the member ID
        if this list is empty, return False
        if not, return True'''
    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        
        # select books currently being borrowed and the member currently borrowing that book
        cursor.execute('SELECT ID, MemberID FROM BookInfo WHERE MemberID = ?', (memberId, ))
        
        membersHolding = cursor.fetchall()
        if len(membersHolding) == 0:
            return False
        else:
            return check_holding_overdue(str(membersHolding[0][1]), membersHolding[0][0])
        conn.commit()
        conn.close()

    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()


def check_holding_overdue(memberId, bookId):
    ''' function that checks whether a member is holding an overdue book or not
        given Member ID and Book ID
         returns True if the book is overdue
         returns False if book is still within loan period'''

    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        
        # select books currently being borrowed and the member currently borrowing that book
        cursor.execute('''SELECT BookID, CheckoutDate
                            FROM LoanHistory WHERE ReturnDate = "" AND BookID = ?''', (bookId, ))
        
        holding = cursor.fetchall()
        checkoutDate = datetime.strptime(holding[0][1], '%Y-%m-%d').date()
        today = datetime.today().date()
        diff = str(abs(checkoutDate - today))
        diff = diff.strip("days, 0:00:00")

        # checking book is still within its loan period
        if int(diff) > int(loan_period(holding[0][0])):
            return True
        else:
            return False
        
        conn.commit()
        conn.close()
        return holding
        
    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()

            

def recommend(memberId):
    ''' function for finding the genre of the book a member has given their memeber ID
        returns the genre for the book they are borrowing '''

    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        
        # select books where Member ID matches
        cursor.execute('SELECT ID, Genre, Author, MemberID FROM BookInfo WHERE MemberID = ?', (memberId, ))
        
        loanee = cursor.fetchall()[0]
        # all we need is the genre element of the list
        genre = (loanee[1])
        
        return genre
    
        conn.commit()
        conn.close()
        
    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()


def loaned_members(memberId):
    ''' function which simply returns True if there is a list of members currently borrowing a book,
        and False if there is no list given member ID'''
    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        
        # select books where Member ID matches
        cursor.execute('SELECT ID, Genre, Author, MemberID FROM BookInfo WHERE MemberID = ?', (memberId, ))
        
        loanee = cursor.fetchall()
        if len(loanee) == 0:
            return False
        else:
            return True
        conn.commit()
        conn.close()
        
    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()
        
        
            
            
def loan_period(bookId):
    ''' function which obtains the Loan Period of a book given the Book ID
        returns the Loan Period'''

    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        
        # select loan period of book, where book IDs match
        cursor.execute('SELECT LoanPeriod FROM BookInfo WHERE ID=?', (bookId, ))
        
        loanPeriod = cursor.fetchall()[0][0]  # only need the first element of the first element of list
        conn.commit()
        return loanPeriod

    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()



def return_overdue(bookId):
    ''' function that checks if unreturned books are past their Loan Period or not given Book ID
        returns True if they are past loan period
        returns False if still within Loan period '''
    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        
        # select books which have not yet been returned and IDs match
        cursor.execute('SELECT * FROM LoanHistory WHERE (BookID == ? AND ReturnDate IS NULL) OR (BookID == ? AND ReturnDate == "")', (bookId, ))

        unreturned = cursor.fetchall()[0] # only need date element of list

        checkoutDate = datetime.strptime(unreturned[2], '%Y-%m-%d').date()
        today = datetime.today().date()
        diff = str(abs(checkoutDate - today))
        diff = diff.strip("days, 0:00:00")

        if int(diff) > int(loan_period(unreturned[1])):
            
            return True # late return
        else:
            return False # returned on time
        conn.commit()

    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()

def overdue_check():
    ''' function which returns a list of all books past their loan period (returned and unreturned) '''

    try:
        conn = sqlite3.connect("Library.db")
        cursor = conn.cursor()
        todayDate = datetime.today().strftime('%Y-%m-%d')
        cursor.execute
        
        # selecting all books which are past their loan period
        cursor.execute('''SELECT
                            BookID,
                            CheckoutDate,
                            IFNULL(ReturnDate, ?),
                            LoanPeriod,
                            ABS(JULIANDAY(CheckoutDate) - JULIANDAY(ReturnDate)) AS diff,
                            ABS(JULIANDAY(CheckoutDate) - JULIANDAY(ReturnDate)) * 0.25 AS CurrentFine
                            FROM LoanHistory
                            INNER JOIN BookInfo on BookInfo.ID = LoanHistory.BookID
                            WHERE ABS(JULIANDAY(CheckoutDate) - JULIANDAY(ReturnDate)) > LoanPeriod''', (todayDate, ))
        overdue = cursor.fetchall()
        return overdue
        conn.commit()
        return 

    except Error as e:
        print (e)
    finally:
        if conn:
            conn.close()
            
            
            
    

if __name__ == '__main__':
    ''' database function calling the reset function when this file is explicitly run'''
    initialise_library()
    reset_database()
    


