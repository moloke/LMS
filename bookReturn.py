''' A Python module which contains functions used to ask the librarian for the ID
    of the book(s) they wish to return and provide either an appropriate error message,
    or a message letting them know they have returned the book(s) successfully. '''

from database import *


def check_overdue(bookId):
    ''' function checking the book being returned isn't being returned late
        done by sending book ID to function in database module

        if on time, return True
        if late, return False '''

    if return_overdue(bookId):
        return False
    else:
        return True
    

def check_valid(bookId):
    ''' function checking book isn't already available
        book must already be on loan in order to return it
        done by sending book ID to function in database module

        if book available, return False
        if book on loan, return True '''

    if book_available(bookId):
        return False
    else:
        return True


def try_book_return(bookId):
    ''' function calling the two success criteria for returning a book

        1. book must already be on loan in order to return it
            if not, return Invalid
        2. user must be notified if book is being returned late
            if so, return Overdue

        if neither, return True (book returned without any problems) '''

    if check_valid(bookId):
        if check_overdue(bookId):
            return True
        else:
            msg = "Overdue"
            return msg
    else:
        msg = "Invalid"
        return msg


