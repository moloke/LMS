''' A Python module which contains functions used to ask the librarian for borrower’s
    member-ID and the ID of the book(s) they wish to withdraw. Then, after performing
    the validity checks and functionality, the program should return a message letting
    the librarian know whether they have withdrawn the book successfully. '''

from database import *


def book_confirm(bookId):
    ''' fucntion which shows user data of book they are about to checkout/return
        done by sending book ID to function in database
        returns a suitable string that can be shown in textbox

        note: this function can be accessed when returning a book as well, thus reducing redundancy '''

    data = get_book_data(bookId)
    msg = ("Book ID: "+ str(data[0]) +"\n"
           "Genre: "+ str(data[1]) +"\n"
           "Title: "+ str(data[2]) +"\n"
           "Author: "+ str(data[3]) +"\n"
           "Loan Period: "+ str(data[4]) +" days \n"
           "Purchase Date: "+ str(data[5]) +"\n"
           "Currently held by: "+ str(data[6]) +"\n")
    
    return str(msg)


def check_overdue(memberId):
    ''' function checking a book isn't being loaned to a member currently holding an overdue book
        done by sending Member ID to function in database

        if holding an overdue book, return False
        if not, return True'''

    if currently_holding(memberId):
        return False
    else:
        return True


def check_book_available(bookId):
    ''' function checking book is not already on loan to someone else
        done by sending book ID to function in database
        returns status of selected book'''
    return book_available(bookId)


def try_book_checkout(memberId, bookId):
    ''' function calling the two success criteria for checking out a book

        1. member must not be holding an overdue book
            if so, return Overdue
        2. book must be available in order to complete checkout
            if not, return Unavailable

        if both okay, return True (book checkout without any problems) '''

    if check_overdue(memberId):
        if check_book_available(bookId):
            return True
        else:
            msg = "Unavailable"
            return msg
    else:
        msg = "Overdue"
        return msg


