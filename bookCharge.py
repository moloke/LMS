''' A Python module which contains functions used to allow the librarian to calculate
members’ fines for the overdue books '''

from database import *

def get_overdue_data():
    ''' function calling overdue function in database
        returns a list of books which are overdue/have been returned late'''
    return overdue_check()


''' this module may seem pointless, but for security reasons an MVC hierarchy must be maintained,
    so the menu module cannot directly access the database module'''
