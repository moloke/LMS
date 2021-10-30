''' A python main program which provides the required menu options to the librarian
for the program functionalities. The menu is based on the Python Graphical User
Interface (namely the tkinter python module).
The GUI uses only one window and is easy to use. '''

import tkinter as tk
from tkinter import *
from tkinter import ttk
from database import *
from bookCheckout import *
from bookReturn import *
from bookCharge import *
from bookRecommend import *
import numpy as np
window = tk.Tk()


# function which resets all buttons, text boxes and labels to allow for new input in "Checkout" tab
def reset_tab1():
    bookDetails.delete('1.0', END)
    bookDetails.grid_remove()
    checkoutBtn.grid_remove()
    confirmBookLbl.grid_remove()
    successCheckLbl.configure(text="")
    bookDetails.grid_remove()
    invalidMILabel.configure(text="")
    invalidBILabel.configure(text="")
    memIdLabel.configure(text = "")
    memberIdBtn['state']='enabled'
    memIdEnt['state']='enabled'
    memIdEnt.delete(0, 'end')
    # showing user what to type in this textbox
    memIdEnt.insert(0, 'Enter Member ID')
    # empty textbox once clicked
    memIdEnt.bind("<FocusIn>", lambda args: memIdEnt.delete('0', 'end'))

    bookIdLabel.configure(text = "")
    bookIdLabel.grid_remove()
    bookIdEnt.grid_remove()
    bookIdBtn.grid_remove()

    bookIdBtn['state']='enabled'
    bookIdEnt['state']='enabled'
    bookIdEnt.delete(0, 'end')
    # showing user what to type in this textbox
    bookIdEnt.insert(0, 'Enter Book ID')
    # empty textbox once clicked
    bookIdEnt.bind("<FocusIn>", lambda args: bookIdEnt.delete('0', 'end'))


# function which resets all buttons, text boxes and labels to allow for new input in "Return" tab
def reset_tab2():
    t2bookDetails.delete('1.0', END)
    t2returnBtn.grid_remove()
    t2bookDetails.grid_remove()
    t2confirmBookLbl.grid_remove()
    t2successReturnLbl.grid_remove()

    t2bookIdBtn['state']='enabled'
    t2bookIdEnt['state']='enabled'
    t2bookIdEnt.delete(0, 'end')
    # showing user what to type in this textbox
    t2bookIdEnt.insert(0, 'Enter Book ID')
    t2bookIdEnt.bind("<FocusIn>", lambda args: t2bookIdEnt.delete('0', 'end'))

            
def member_id_check():

    ''' checking that member ID input is valid
        only alphabetic characters allowed (no numbers, spaces or symbols)
        must be exactly 4 characters as with all member IDs

        if not, show appropriate warning message in corresponding label
        if so, allow to continue to enter book ID '''

    if memberId.get().isalpha():
        if len(memberId.get()) == 4:
            memIdLabel.configure(text = "Member Id: "+memberId.get())
            invalidMILabel.configure(text="")
            memberIdBtn['state']='disabled'
            memIdEnt['state']='disabled'

            bookIdLabel.grid()
            bookIdEnt.grid()
            bookIdBtn.grid()
        else:
            invalidMILabel.configure(text="Invalid Member ID, must be in **** form", foreground="red")
    else:
        invalidMILabel.configure(text="Invalid Member ID, must be in **** form", foreground="red")


def book_id_check():

    ''' checking that book ID input is valid
            only integer characters allowed (no decimals, letters or symbols)
            must lie in the range 1-20 (inclusive) as book IDs only go up to 20

            if not, show appropriate warning message in corresponding label
            if so, show corresponding book details in textbox '''

    if bookId.get().isdigit():
        if 1 <= (int(bookId.get())) <= 20:
            bookIdLabel.configure(text = "Book Id: "+bookId.get())
            invalidBILabel.configure(text="")
            bookIdBtn['state']='disabled'
            bookIdEnt['state']='disabled'
            memIdEnt['state']='disabled'
            confirmBookLbl.grid()
            bookDetails.grid()
            
            checkoutBtn.grid()
            
            bookdata = book_confirm(bookId.get())
            bookDetails.delete('1.0', END)
            bookDetails.insert('1.0', bookdata)

        else:
            invalidBILabel.configure(text="Invalid Book ID, 1 - 20", foreground="red")
    else:
        invalidBILabel.configure(text="Invalid Book ID, 1 - 20", foreground="red")



def t2book_id_check():

    ''' checking that member ID input is valid
            only alphabetic characters allowed (no numbers, spaces or symbols)
            must be exactly 4 characters as with all member IDs

            if not, show appropriate warning message in corresponding label
            if so, show corresponding book details in text box '''

    if t2bookId.get().isdigit():
        if 1 <= (int(t2bookId.get())) <= 20:
            t2bookIdLabel.configure(text = "Book Id: "+t2bookId.get())
            t2invalidBILabel.configure(text="")
            t2bookIdBtn['state']='disabled'
            t2bookIdEnt['state']='disabled'
            
            t2confirmBookLbl.grid()
            t2bookDetails.grid()
            t2returnBtn.grid()

            bookdata = book_confirm(t2bookId.get())
            t2bookDetails.delete('1.0', END)
            t2bookDetails.insert('1.0', bookdata)
            
        else:
            t2invalidBILabel.configure(text="Invalid Book ID, 1 - 20", foreground="red")
    else:
        t2invalidBILabel.configure(text="Invalid Book ID, 1 - 20", foreground="red")


def checkout_book():

    ''' function called once all validity tests have been passed
        calling function in bookCheckout module

        display corresponding error/success message when user tries to checkout book '''

    if try_book_checkout(memberId.get(), bookId.get()) == "Unavailable":
        successCheckLbl.configure(text = "Book unavailable as already on loan", foreground="red")
    elif try_book_checkout(memberId.get(), bookId.get()) == "Overdue":
        successCheckLbl.configure(text = "Member currently holding an overdue book", foreground="red")
        
    else:
        dbcheckout_book(memberId.get(), bookId.get())
        successCheckLbl.configure(text = "Book successfully withdrawn!", foreground="green")


def return_book():

    ''' function called once all validity tests have been passed
            calling function in bookReturn module

            display corresponding error/success message when user tries to return book '''

    if try_book_return(t2bookId.get()) == "Invalid":
        t2successReturnLbl.configure(text = "This book hasn't been checked out", foreground="red")
        t2successReturnLbl.grid()
    elif try_book_return(t2bookId.get()) == "Overdue":
        t2successReturnLbl.configure(text = "This book has been returned late", foreground="orange")
        t2successReturnLbl.grid()
        dbreturn_book(t2bookId.get())
    else:
        dbreturn_book(t2bookId.get())
        t2successReturnLbl.grid()
        t2successReturnLbl.configure(text = "Book successfully returned!", foreground="green")



def charges():

    ''' function called when user wants to view all overdue books and fines

        calling function in bookCharge module
        retrieves bookCharge data and converts to appropriate string for the listbox line by line '''

    chargeList = get_overdue_data()
    nextNum = 1
    totFine = 0
    for x in range(len(chargeList)):
        overdueList.insert(nextNum, ("BookID: "+str(chargeList[x][0]) +
                                     ", Loan Period: "+str(chargeList[x][3]) + " days" +
                                     ", "+str(int(chargeList[x][4])) + " days late"
                                     ", Current fine: £"+str(chargeList[x][5])))
        totFine = totFine + chargeList[x][5]
        nextNum=+1
    
    totalList.insert(1, ("£"+str(totFine)))


def recmember_id_check():

    ''' checking that member ID input is valid
            only alphabetic characters allowed (no numbers, spaces or symbols)
            must be exactly 4 characters as with all member IDs

            if not, show appropriate warning message in corresponding label
            if so, check that member is currently borrowing a book
                do this by calling function in bookRecommend module
                if not, then we cannot recommend a book as no data on member
                    show appropriate failure message in corresponding label
                if so, then we can recommend a book based on the genre of the book they are borrowing
                    do this by calling function in bookRecommend module'''

    if recmemberId.get().isalpha():
        if len(recmemberId.get()) == 4:
            recmemIdLabel.configure(text = "Member Id: "+recmemberId.get())
            recinvalidMILabel.configure(text="")

            if check_holders(recmemberId.get()):
                recdata = recommended_books(recmemberId.get())
                recommendList.grid()
                recommendList.delete('1.0', END)
                recommendList.insert('1.0', recdata)
            else:
                recinvalidMILabel.configure(text="Sorry, this member is not\ncurrently borrowing a book", foreground="orange")
                recommendList.grid_remove()
        else:
            recinvalidMILabel.configure(text="Invalid Member ID, must be in **** form", foreground="red")
            recommendList.grid_remove()
    else:
        recinvalidMILabel.configure(text="Invalid Member ID, must be in **** form", foreground="red")
        recommendList.grid_remove()


# setting window attributes
window.title("Library Management System")  # title of window
window.geometry('900x600+200+100')  # size and position of window

# setting tab control and setting the four tabs for the four possible operations
tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

# titling each of the tabs with their corresponding operations
tabControl.add(tab1, text="Checkout Book")
tabControl.add(tab2, text="Return Book")
tabControl.add(tab3, text="Overdue Books")
tabControl.add(tab4, text="Recommend Books")
tabControl.pack(expand = 1, fill="both", padx=10, pady=10)



##################### all GUI elements inside "Checkout book" tab ###############################


ttk.Label(tab1,
           text="Member ID and Book ID required to checkout books").grid(column = 0,
                                                       row = 0,
                                                       padx = 30,
                                                       pady = 30)
memIdLabel = ttk.Label(tab1, text = "Enter Member ID")
memIdLabel.grid(column = 0, row = 1)

memberId = tk.StringVar()


memIdEnt = ttk.Entry(tab1, width = 25, textvariable = memberId)
memIdEnt.grid(column = 0, row = 2)
memIdEnt.insert(0, 'Enter Member ID')
memIdEnt.bind("<FocusIn>", lambda args: memIdEnt.delete('0', 'end'))

memberIdBtn = ttk.Button(tab1, text = "Next", command = member_id_check)
memberIdBtn.grid(column=2, row=2)

invalidMILabel = ttk.Label(tab1, text="")
invalidMILabel.grid(column = 3, row = 2)

bookIdLabel = ttk.Label(tab1, text = "Enter Book ID")
bookIdLabel.grid(column = 0, row = 5)
bookIdLabel.grid_remove()

bookId = tk.StringVar()

bookIdEnt = ttk.Entry(tab1, width = 25, textvariable = bookId)
bookIdEnt.grid(column = 0, row = 6)
bookIdEnt.insert(0, 'Enter Book ID')
bookIdEnt.bind("<FocusIn>", lambda args: bookIdEnt.delete('0', 'end'))
bookIdEnt.grid_remove()

bookIdBtn = ttk.Button(tab1, text = "Next", command = book_id_check)
bookIdBtn.grid(column=2, row=6)
bookIdBtn.grid_remove()

invalidBILabel = ttk.Label(tab1, text="")
invalidBILabel.grid(column = 3, row = 6)

resetBtn = ttk.Button(tab1, text = "Reset", command = reset_tab1)
resetBtn.grid(column=0, row=7)

confirmBookLbl = ttk.Label(tab1, text="Check and confirm this is the correct book:")
confirmBookLbl.grid(column=3, row=1)
confirmBookLbl.grid_remove()

bookDetails = tk.Text(tab1, height=10, width=50)
bookDetails.grid(column = 3, row=2)
bookDetails.grid_remove()

checkoutBtn = ttk.Button(tab1, text = "Checkout Book", command = checkout_book)
checkoutBtn.grid(column=3, row=3)
checkoutBtn.grid_remove()


successCheckLbl = ttk.Label(tab1, text="")
successCheckLbl.grid(column=3, row=4)



####################### all GUI elements inside "Return book" tab ################################


ttk.Label(tab2,
           text="Book Returns").grid(column = 0,
                                                       row = 0,
                                                       padx = 30,
                                                       pady = 30)

t2bookIdLabel = ttk.Label(tab2, text = "Input book ID")
t2bookIdLabel.grid(column = 0, row = 1)

t2bookId = tk.StringVar()

t2bookIdEnt = ttk.Entry(tab2, width = 15, textvariable = t2bookId)
t2bookIdEnt.grid(column = 0, row = 2)
t2bookIdEnt.insert(0, 'Enter Book ID')
t2bookIdEnt.bind("<FocusIn>", lambda args: t2bookIdEnt.delete('0', 'end'))

t2bookIdBtn = ttk.Button(tab2, text = "Next", command = t2book_id_check)
t2bookIdBtn.grid(column=2, row=2)

t2invalidBILabel = ttk.Label(tab2, text="")
t2invalidBILabel.grid(column = 3, row = 2)

t2resetBtn = ttk.Button(tab2, text = "Reset", command = reset_tab2)
t2resetBtn.grid(column=0, row=7)

t2confirmBookLbl = ttk.Label(tab2, text="Check and confirm this is the correct book:")
t2confirmBookLbl.grid(column=3, row=1)
t2confirmBookLbl.grid_remove()

t2bookDetails = tk.Text(tab2, height=10, width=50)
t2bookDetails.grid(column = 3, row=2)
t2bookDetails.grid_remove()

t2returnBtn = ttk.Button(tab2, text = "Return Book", command = return_book)
t2returnBtn.grid(column=3, row=3)
t2returnBtn.grid_remove()

t2successReturnLbl = ttk.Label(tab2, text="")
t2successReturnLbl.grid(column=3, row=4)



####################### all GUI elements inside "Overdue books" tab ###############################


ttk.Label(tab3,
           text="List of overdue books:").grid(column = 0,
                                                       row = 0,
                                                       padx = 30,
                                                       pady = 30)

overdueBtn = ttk.Button(tab3, text = "Display overdue books", command = charges)
overdueBtn.grid(column=1, row=0)

overdueList = tk.Listbox(tab3, height=28, width=80)
overdueList.grid(column = 1, row=1)

totalLbl = ttk.Label(tab3, text="Book fines total:")
totalLbl.grid(column=2, row=1)

totalList = tk.Listbox(tab3, height=1, width=10)
totalList.grid(column=3, row=1) 


####################### all GUI elements inside "Recommend books" tab ##############################


ttk.Label(tab4,
           text="List of recommended books for...").grid(column = 0,
                                                       row = 0,
                                                       padx = 30,
                                                       pady = 30)

recmemIdLabel = ttk.Label(tab4, text = "Enter Member ID")
recmemIdLabel.grid(column = 1, row = 0)

recmemberId = tk.StringVar()

recmemIdEnt = ttk.Entry(tab4, width = 25, textvariable = recmemberId)
recmemIdEnt.grid(column = 1, row = 1)
recmemIdEnt.insert(0, 'Enter Member ID')
recmemIdEnt.bind("<FocusIn>", lambda args: recmemIdEnt.delete('0', 'end'))

recommendBtn = ttk.Button(tab4, text = "Recommend", command = recmember_id_check)
recommendBtn.grid(column=2, row=1)

recinvalidMILabel = ttk.Label(tab4, text="")
recinvalidMILabel.grid(column = 3, row = 1)

recommendList = tk.Text(tab4, height=20, width=65)
recommendList.grid(column = 0, row=2)
recommendList.grid_remove()



window.mainloop()
