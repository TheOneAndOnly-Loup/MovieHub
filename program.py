import csv
import ast

MOVIES_FILE = "movies.csv"
LINE = "-----------------------------------------------"
SHORT_LINE = "---------------"


# ---------------------------------------------------------------
# Movie: holds the information about one film
# ---------------------------------------------------------------
class Movie:
    def __init__(self, id, title, year, genre, avg_rating, number_of_ratings, sum_of_ratings, reviews):
        self.id = id
        self.title = title
        self.year = year
        self.genre = genre
        self.avg_rating = avg_rating
        self.number_of_ratings = number_of_ratings
        self.sum_of_ratings = sum_of_ratings
        self.reviews = reviews  # a list of [user_id, review_text]

    def __str__(self):
        return f"{self.id}: {self.title} ({self.year}) - {self.genre} - {self.avg_rating}/10"

    def add_rating(self, value):
        self.sum_of_ratings += value
        self.number_of_ratings += 1
        self.avg_rating = round(self.sum_of_ratings / self.number_of_ratings, 2)

    def add_review(self, user_id, text):
        self.reviews.append([user_id, text])


# ---------------------------------------------------------------
# User: someone who can rate and review movies
# ---------------------------------------------------------------
class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.reviews = {}  # movie title -> review text


# ---------------------------------------------------------------
# MovieHub: stores all the movies and users
# ---------------------------------------------------------------
class MovieHub:
    def __init__(self):
        self.movies = []
        self.users = []
        self.load_movies()

    # --- Saving and loading -----------------------------------

    def load_movies(self):
        with open(MOVIES_FILE, "r") as file:
            reader = csv.reader(file)
            self.headers = next(reader)  # the first line holds the column names

            for row in reader:
                movie = Movie(
                    id=int(row[0]),
                    title=row[1],
                    year=int(row[2]),
                    genre=row[3],
                    avg_rating=float(row[4]),
                    number_of_ratings=int(row[5]),
                    sum_of_ratings=int(row[6]),
                    # The reviews are saved as text like "[[0, 'great']]".
                    # literal_eval turns that text back into a real list.
                    reviews=ast.literal_eval(row[7]),
                )
                self.movies.append(movie)

    def save_movies(self):
        with open(MOVIES_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)

            for movie in self.movies:
                writer.writerow([
                    movie.id,
                    movie.title,
                    movie.year,
                    movie.genre,
                    movie.avg_rating,
                    movie.number_of_ratings,
                    movie.sum_of_ratings,
                    movie.reviews,
                ])

    # --- Finding things ---------------------------------------

    def find_movie_by_id(self, movie_id):
        for movie in self.movies:
            if movie.id == movie_id:
                return movie
        return None

    def find_movies_by_title(self, text):
        found = []
        for movie in self.movies:
            if text.lower() in movie.title.lower():
                found.append(movie)
        return found

    def find_movies_by_genre(self, genre):
        found = []
        for movie in self.movies:
            if movie.genre.lower() == genre.lower():
                found.append(movie)
        return found

    def find_user_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_all_genres(self):
        genres = []
        for movie in self.movies:
            if movie.genre not in genres:
                genres.append(movie.genre)
        return sorted(genres)

    def get_highest_rated(self):
        return max(self.movies, key=lambda movie: movie.avg_rating)

    # --- Users ------------------------------------------------

    def sign_up(self, name):
        new_id = len(self.users)
        new_user = User(new_id, name)
        self.users.append(new_user)
        return new_user


# ---------------------------------------------------------------
# Small helpers for reading what the user types
# ---------------------------------------------------------------
def ask_for_number(question):
    """Keep asking until the user types a whole number."""
    while True:
        answer = input(question)
        if answer.isdigit():
            return int(answer)
        print("Please type a number.")


def print_movies(movies):
    if len(movies) == 0:
        print("No movies found.")
    for movie in movies:
        print(movie)


def ask_for_movie(hub):
    """Show every movie and let the user pick one by its ID."""
    print_movies(hub.movies)
    movie_id = ask_for_number("\nEnter the movie ID: ")
    movie = hub.find_movie_by_id(movie_id)
    if movie is None:
        print("There is no movie with that ID.")
    return movie


# ---------------------------------------------------------------
# One function per menu option
# ---------------------------------------------------------------
def sign_up(hub):
    name = input("Choose a username: ")
    user = hub.sign_up(name)
    print(f"Welcome {user.name}! Your user ID is {user.id}.")


def log_in(hub):
    if len(hub.users) == 0:
        print("Nobody has signed up yet.")
        return None

    for user in hub.users:
        print(f"ID: {user.id}  {user.name}")

    user_id = ask_for_number("Please enter your user ID: ")
    user = hub.find_user_by_id(user_id)
    if user is None:
        print("There is no user with that ID.")
    else:
        print(f"Logged in as {user.name}.")
    return user


def search_movie(hub):
    text = input("Search by title: ")
    print_movies(hub.find_movies_by_title(text))


def show_highest_rated(hub):
    movie = hub.get_highest_rated()
    print(f"Highest rated movie: {movie}")


def rate_movie(hub, user):
    movie = ask_for_movie(hub)
    if movie is None:
        return

    rating = ask_for_number("Enter a rating between 1 and 10: ")
    if rating < 1 or rating > 10:
        print("The rating must be between 1 and 10.")
        return

    movie.add_rating(rating)
    hub.save_movies()
    print(f"Thanks! {movie.title} now has an average of {movie.avg_rating}/10.")


def review_movie(hub, user):
    movie = ask_for_movie(hub)
    if movie is None:
        return

    text = input("Write your review:\n")
    movie.add_review(user.id, text)
    user.reviews[movie.title] = text
    hub.save_movies()
    print("Your review has been saved.")


def show_my_reviews(user):
    if len(user.reviews) == 0:
        print("You haven't written any reviews yet.")
    for title, text in user.reviews.items():
        print(f"{title} - {text}\n")


def filter_by_genre(hub):
    genres = hub.get_all_genres()
    for number, genre in enumerate(genres):
        print(f"{number}. {genre}")

    choice = ask_for_number("\nPlease select a genre: ")
    if choice >= len(genres):
        print("That is not one of the genres.")
        return

    print_movies(hub.find_movies_by_genre(genres[choice]))


# ---------------------------------------------------------------
# Main program
# ---------------------------------------------------------------
MENU = """Welcome to MovieHub! What would you like to do?
    1. Sign up
    2. Log in
    3. Search for a movie
    4. Display movies
    5. Display highest rated movie
    6. Rate a movie
    7. Review a movie
    8. View your reviews
    9. Filter by genre
    10. Exit
"""


def main():
    hub = MovieHub()
    current_user = None  # nobody is logged in at the start

    print(LINE)
    while True:
        print(MENU)
        choice = ask_for_number(": ")
        print(SHORT_LINE)

        # Options 6, 7 and 8 need someone to be logged in
        if choice in [6, 7, 8] and current_user is None:
            print("Please log in first.")
            print(LINE)
            continue

        if choice == 1:
            sign_up(hub)
        elif choice == 2:
            user = log_in(hub)
            if user is not None:
                current_user = user
        elif choice == 3:
            search_movie(hub)
        elif choice == 4:
            print_movies(hub.movies)
        elif choice == 5:
            show_highest_rated(hub)
        elif choice == 6:
            rate_movie(hub, current_user)
        elif choice == 7:
            review_movie(hub, current_user)
        elif choice == 8:
            show_my_reviews(current_user)
        elif choice == 9:
            filter_by_genre(hub)
        elif choice == 10:
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 10.")

        print(LINE)


# Only start the menu when this file is run directly
if __name__ == "__main__":
    main()
