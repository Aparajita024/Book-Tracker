import numpy as np

def addBook():
  print("\nEnter details of the book")
  title = input("Title: ").strip().lower()
  author = input("Author: ").strip().lower()
  genre = input("Genre: ").strip().lower()
  status = input("Status(read/unread): ").strip().lower()
  if status == 'read':
    try:
        rating = float(input("Rating(out of 5): "))
    except ValueError:
        print("Invalid rating! Setting rating to 0.")
        rating = 0.0
  else:
    rating = '-'
  book ={'title' : title,
      'author' : author,
      'genre' : genre,
      'status' : status,
      'rating' : rating}

  return book

def updateBook(book) :
  book['status'] = 'read'
  try:
    rating = float(input("Rating(out of 5): "))
  except ValueError:
    print("Invalid rating! Keeping previous rating.")
    rating = book['rating']
  book['rating'] = rating
  print("\nBook Updated Successfully!")
  return book

def showAllBooks(books) :
  print(f"\n{'All Books' :-^50}")
  for i,book in enumerate(books, start=1) :
    print(f"\n ({i}){book['title'].title()} \n Author: {book['author'].capitalize()} \n Genre: {book['genre'].capitalize()} \n Status : {book['status'].capitalize()} \n Rating : {book['rating']}")

def filterBook(filter_by,books) :
  book = []
  if filter_by == "title" :
    title = input("\nTitle: ").strip().lower()
    book = list(filter(lambda x : x['title'] == title, books))

  elif filter_by == 'author' :
    author = input("\nAuthor: ").strip().lower()
    book = list(filter(lambda x : x['author'] == author, books))

  elif filter_by == 'status' :
    status = input("Read/Unread? ").strip().lower()
    book = list(filter(lambda x : x['status'] == status, books))

  elif filter_by == 'genre' :
    genre = input("Genre: ").strip().lower()
    book = list(filter(lambda x : x['genre'] == genre, books))

  elif filter_by == 'rating' :
    rating = float(input("Rating: "))
    book = list(filter(lambda x : type(x['rating']) == float and x['rating'] >= rating , books))

  else :
    print("Invalid Input!")
    filter_by = input("Search by (title/author/status/genre/rating): ").strip().lower()
    filterBook(filter_by, books)

  if book :
    print("\nBooks Found!")
    for b in book :
      print(f"\n {b['title'].title()} \n Author: {b['author'].capitalize()} \n Genre: {b['genre'].capitalize()} \n Status : {b['status'].capitalize()} \n Rating : {b['rating']}")

  else :
    print("Book Not Found!")

def summary(books) :
  summary = {}
  summary['Total Number of Books'] = len(books)
  read = list(map(lambda x : 1 if x['status'] == 'read' else 0, books ))
  summary['Number of Books read'] = np.sum(read)
  unread = list(map(lambda x : 1 if x['status'] == 'unread' else 0, books ))
  summary['Number of Books unread'] = np.sum(unread)
  rating = list(map(lambda x : x['rating'] if type(x['rating']) == float else 0, books))
  summary['Average Rating'] = np.average(rating) if rating else 0
  for book in books :
    if book['rating'] == max(rating) :
      summary['Highest Rated Book'] = book['title']
  countGenre = {}
  for book in books :
    value = book['genre']
    if value in countGenre :
      countGenre[value] += 1
    else :
      countGenre[value] = 1
  maxGenre = max(countGenre.values())
  genre = []
  for key, value in countGenre.items() :
    if maxGenre == value :
      genre.append(key)
  if len(countGenre) == len(genre) :
    summary['Most read genre'] = 'None'
  else :
    summary['Most read genre'] = genre
  printSummary(summary, countGenre)

def printSummary(summary , countGenre) :
  for key, value in summary.items() :
    print()
    if key != 'Most read genre' :
      print(f" {key} = {value}")
    else :
      print(f" {key} = {','.join(value)} ")
  print("\n All Genres")
  for key , value in countGenre.items() :
    print(f" {key} : {value}")

books = []
print(f"{'Welcome to Book Tracker!'}")
while True :
  print(f"\n{'MENU':-^30} \n 1.Add Book \n 2.Update Book \n 3.Show All Books \n 4.Search Book by Category \n 5.Summary \n 6.Exit")
  try :
    choice = int(input("Your Choice = "))
    if choice < 1 or choice > 6 :
      raise ValueError("Invalid Choice! Choose an integer between 1 to 6")
  except ValueError as e :
    print("ValueError:",e)
    continue

  if choice == 1 :
    books.append(addBook())
    print("\nBook Added!")

  elif choice == 2 :
    try :
      if books:
        title = input("\nWhich book to update? ")
        try :
          found = False
          for book in books :
            if book['title'] == title :
              updateBook(book)
              found = True
              break
          if not found :
            raise ValueError("Book does not exist in the list")
        except ValueError as e :
            print("\nValueError:",e)
      else :
        raise ValueError("\nNo books added yet!")
    except ValueError as e :
      print("\nValueError:",e)

  elif choice == 3:
    showAllBooks(books)

  elif choice == 4 :
    filter_by = input("Search by (title/author/status/genre/rating): ").strip().lower()
    filterBook(filter_by, books)

  elif choice == 5 :
    summary(books)

  else :
    print("\nThankYou!")
    break