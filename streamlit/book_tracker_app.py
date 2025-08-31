import streamlit as st
import numpy as np

if 'books' not in st.session_state:
    st.session_state['books'] = []

def add_book():
    st.subheader("Add a New Book")
    with st.form(key='add_book_form'):
        title = st.text_input("Title").strip().lower()
        author = st.text_input("Author").strip().lower()
        genre = st.text_input("Genre").strip().lower()
        status = st.selectbox("Status", ['Select','read', 'unread'])
        rating = None
        if status == 'read':
            rating = st.slider("Rating (out of 5)", 0.0, 5.0, 0.0, 0.1, disabled=(status != 'read'))
        submitted = st.form_submit_button("Add Book")
        if submitted:
            if not title or not author or not genre or status != ('read' or 'unread') :
                st.error("Title, Author, Genre and Status cannot be empty!")
            if rating == 0.0 :
                st.error("Rating cannot be zero!")
            else:
                book = {
                    'title': title,
                    'author': author,
                    'genre': genre,
                    'status': status,
                    'rating': rating if rating is not None else '-'
                }
                st.session_state.books.append(book)
                st.success(f"Book '{title.title()}' added!")

def update_book():
    st.subheader("Update Book Status and Rating")
    if not st.session_state.books:
        st.warning("No books added yet to update.")
        return

    titles = [book['title'] for book in st.session_state.books]
    selected_title = st.selectbox("Select Book to Update", titles)
    if selected_title:
        for book in st.session_state.books:
            if book['title'] == selected_title:
                with st.form(key='update_book_form'):
                    status = st.selectbox("Status", ['read', 'unread'], index=0 if book['status']=='read' else 1)
                    rating = book['rating'] if book['rating'] != '-' else 3.0
                    if status == 'read':
                        rating = st.slider("Rating (out of 5)", 0.0, 5.0, float(rating), 0.1)
                    else:
                        rating = '-'
                    submitted = st.form_submit_button("Update Book")
                    if submitted:
                        book['status'] = status
                        book['rating'] = rating
                        st.success(f"Book '{selected_title.title()}' updated!")

def show_all_books():
    st.subheader("All Books")
    if not st.session_state.books:
        st.info("No books added yet.")
        return

    for i, book in enumerate(st.session_state.books, start=1):
        st.markdown(f"""
        **{i}. {book['title'].title()}** \n
        Author: {book['author'].capitalize()} \n
        Genre: {book['genre'].capitalize()} \n
        Status: {book['status'].capitalize()} \n
        Rating: {book['rating']}
        """)

def filter_books():
    st.subheader("Search Books")
    if not st.session_state.books:
        st.info("No books added yet.")
        return

    filter_by = st.selectbox("Search by", ['title', 'author', 'status', 'genre', 'rating'])
    filtered_books = []

    if filter_by == 'title':
        title = st.text_input("Enter Title to search").strip().lower()
        if st.button("Search by Title"):
            filtered_books = list(filter(lambda x: x['title'] == title, st.session_state.books))

    elif filter_by == 'author':
        author = st.text_input("Enter Author to search").strip().lower()
        if st.button("Search by Author"):
            filtered_books = list(filter(lambda x: x['author'] == author, st.session_state.books))

    elif filter_by == 'status':
        status = st.selectbox("Select Status", ['read', 'unread'])
        if st.button("Search by Status"):
            filtered_books = list(filter(lambda x: x['status'] == status, st.session_state.books))

    elif filter_by == 'genre':
        genre = st.text_input("Enter Genre to search").strip().lower()
        if st.button("Search by Genre"):
            filtered_books = list(filter(lambda x: x['genre'] == genre, st.session_state.books))

    elif filter_by == 'rating':
        rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1)
        if st.button("Search by Rating"):
            filtered_books = list(filter(lambda x: isinstance(x['rating'], float) and x['rating'] >= rating, st.session_state.books))

    if filtered_books:
        st.success(f"{len(filtered_books)} Book(s) Found:")
        for book in filtered_books:
            st.markdown(f"""
            **{book['title'].title()}**
            Author: {book['author'].capitalize()}
            Genre: {book['genre'].capitalize()}
            Status: {book['status'].capitalize()}
            Rating: {book['rating']}
            """)
    else:
        if st.button("Search"):
            st.error("No books found matching criteria.")

def summary():
    st.subheader("Books Summary")
    books = st.session_state.books
    if not books:
        st.info("No books added yet.")
        return

    total_books = len(books)
    read_count = sum(1 for b in books if b['status'] == 'read')
    unread_count = total_books - read_count
    ratings = [b['rating'] for b in books if isinstance(b['rating'], float)]
    avg_rating = np.average(ratings) if ratings else 0
    highest_rating = max(ratings) if ratings else 0
    highest_rated_books = [b['title'] for b in books if b['rating'] == highest_rating]

    genre_count = {}
    for book in books:
        genre_count[book['genre']] = genre_count.get(book['genre'], 0) + 1

    max_genre_count = max(genre_count.values()) if genre_count else 0
    most_read_genres = [g for g, count in genre_count.items() if count == max_genre_count] if max_genre_count > 0 else []

    st.markdown(f"""
    - Total Number of Books: **{total_books}**
    - Number of Books Read: **{read_count}**
    - Number of Books Unread: **{unread_count}**
    - Average Rating: **{avg_rating:.2f}**
    - Highest Rated Book(s): **{', '.join([title.title() for title in highest_rated_books])}**
    - Most Read Genre(s): **{', '.join(most_read_genres) if most_read_genres else 'None'}**
    """)

    st.markdown("All Genres and Counts:")
    for genre, count in genre_count.items():
        st.write(f"- {genre.capitalize()}: {count}")

st.title("Book Tracker App")

menu = ["Add Book", "Update Book", "Show All Books", "Search Books", "Summary"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Book":
    add_book()
elif choice == "Update Book":
    update_book()
elif choice == "Show All Books":
    show_all_books()
elif choice == "Search Books":
    filter_books()
elif choice == "Summary":
    summary()