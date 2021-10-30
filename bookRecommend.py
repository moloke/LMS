''' A Python module which contains functions used to list the recommended books
for a member according to the genre of the book they are currently borrowing'''

from database import *

def check_holders(memberId):

    ''' function to check if member is currently borrowing a book
        done by calling function in database module

        if so, return True
        if not, return False'''

    if loaned_members(memberId):
        return True
    else:
        return False


def recommended_books(recmemberId):
    ''' function to recommend books by calling function in database to retrieve genre
        of book the member is currently borrowing

        send this genre to genre_rec() function to obtain corresponding list of books to recommend
        returns this list of books as string '''

    genre = recommend(recmemberId)
    return genre_rec(genre)
    
    
def genre_rec(genre):
    ''' returning appropriate list of books to recommend according to the genre it was passed
        each of the five genres will return its own list of recommended books for that genre '''

    if genre == "Sci-Fi":
        scifiList = ('''1. Dune by Frank Herbert
2. Nineteen Eighty-Four by George Orwell 
3. Fahrenheit 451 by Ray Bradbury 
4. The Martian by And Weir 
5. Snow Crash by Neal Stephenson''')
        
        return scifiList
    
    elif genre == "Romance":
        romanceList = ('''1. Pride and Prejudice by Jane Austen
2. The Hating Game: A Novel by Sally Thorne 
3. Jane Eyre by Charlotte Bronte 
4. The Notebook by Nicholas Sparks 
5. The Duke and I by Julia Quinn''')
        
        return romanceList
    
    elif genre == "Fantasy":
        fantasyList = ('''1. The Name of the Wind by Patrick Rothfuss
2. The Way of Kings by Brandon Sanderson 
3. The Fifth Season by N. K. Jemisin 
4. A Game of Thrones by George R. R. Martin 
5. The Lies of Locke Lamora by Scott Lynch''')
        
        return fantasyList
    
    elif genre == "Nonfiction":
        nonfictionList = ('''1. Sapiens: A Brief History of Humankind by Yuval Noah Harari
2. Between the World and Me by Ta-Nehisi Coates 
3. In Cold Blood by Truman Capote 
4. The Immortal Life of Henrietta Lacks by Rebecca Skloot 
5. When Breath Becomes Air by Paul Kalanithi''')
        
        return nonfictionList
    
    elif genre == "Crime Thriller":
        crimethrillerList = ('''1. The Thursday Murder Club by Richard Osman
2. Over My Dead Body by Jeffery Archer 
3. The Girl with the Dragon Tattoo by Stieg Larsson 
4. The Man Who Died Twice by Richard Osman 
5. Apples Never Fall by Liane Moriarty''')
        
        return crimethrillerList

