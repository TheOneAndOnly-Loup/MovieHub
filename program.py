class Database:
    def __init__(self):
        self.films = []
        self.users = []
        self.number_of_users = 0

    # Movie management
    def add_movie(self, movie_obj):
        self.films.append(movie_obj)
    def remove_movie(self, movie_obj):
        self.films.remove(movie_obj)

    # Display functions
    def display_movies(self):
        for i in range(len(self.films)):
            print(f"{i} {self.films[i]}\n")

    def display_highest_rated(self):
        highest_rated = max(self.films, key=lambda film: film.avg_rating)
        print(highest_rated.name)

    def display_reviews(self, user):
        for x, y in user.reviews.items():
            print(f"{x.name} - {y}\n")

    def display_users(self):
        for x in range(len(self.users)):
            print(f"ID:{self.users[x].id} {self.users[x].name}")

    # Search and filter functions
    def search_movie(self):
        search = input("Search by name: ")
        for i in range(len(self.films)): # linear_search, put a more efficient one
            try:
                if self.films[i].name == search:
                    print("Movie found")
            except ValueError:
                print("Movie not found!")
    def filter_by_genre(self, genre):
        filtered_movies = [movie.name for movie in self.films if movie.genre.lower() == genre.lower()]
        for x in filtered_movies:
            print(f"{x}\n")

    # User management
    def sign_up(self, username):
       new_user = User(username, self.number_of_users)

       self.number_of_users += 1
       self.users.append(new_user)

class Film:
    def __init__(self, name, age_rating, genre, year):
        self.name = name
        self.age_rating = age_rating
        self.genre = genre
        self.year = year
        self.reviews = [] # if no rating has been added, the movie will show 0/10... fix this later
        self.ratings = 0
        self.sum=0
        self.avg_rating = 0 # review later
    def __str__(self):
        return f"{self.name} ({self.year}) - {self.genre} - {self.age_rating} - {self.avg_rating}/10"

    # for reviews and ratings: add a way to assign a rating/review to a specific user
    def add_review(self, text): 
        self.reviews.append(text)
    def change_rating(self, value):
        self.sum += value
        self.ratings += 1
        self.avg_rating = round(self.sum / self.ratings, 2)  # average rating

class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.reviews = {}

    def rate(self): # add user-review matching
        movie_hub.display_movies()
        index = int(input("Enter the movie index: "))

        if index > len(movie_hub.films) - 1 or index < 0:
            raise Exception("Invalid index")
        movie_obj = movie_hub.films[index]
        
        value = int(input("Enter a rating between 1 and 10: "))
        if value > 10 or value <= 0:
            raise Exception("Invalid input")
        movie_obj.change_rating(value)

    def review(self): # here as well
        movie_hub.display_movies()
        index = int(input("Enter the movie index: "))

        if index > len(movie_hub.films) - 1 or index < 0:
            raise Exception("Invalid index")
        movie_obj = movie_hub.films[index]

        text = input("Write your review: \n")
        self.reviews.update({movie_obj: text})

        movie_obj.add_review(text)

    def display_reviews(self):
        for i in range(len(self.reviews)):
            print(f"{i}\n")

# Initialising Database object
movie_hub = Database() 

# Initialising movie objects
starwars = Film("Star Wars: A New Hope", "PG", "Sci-Fi", 1977)
godfather = Film("The Godfather", "R", "Crime", 1972)
dark_knight = Film("The Dark Knight", "PG-13", "Action", 2008)

# Initialising user objects
# user1 = User("Joe", 1)
# user2 = User("Jane", 2)
# user3 = User("John", 3)
# user4 = User("Jill", 4)
# user5 = User("Jack", 5)
# user6 = User("Jenny", 6)

# Adding movies to movie_hub database
movie_hub.add_movie(starwars)
movie_hub.add_movie(godfather)
movie_hub.add_movie(dark_knight)

selected_user = None

print("-----------------------------------------------")        

while True:
    print("""Welcome to MovieHub! What would you like to do?
    1. Sign up
    2. Log in
    3. Search for a movie
    4. Display movies
    5. Display highest rated movie
    6. Rate a movie
    7. Review a movie
    8. View your reviews
    9. Filter by genre
    10. Exit\n""")

    menu_choice = int(input(": "))

    if menu_choice == 1:
        print("---------------")
        movie_hub.sign_up(input("Choose a username: "))

    elif menu_choice == 2:
        print("---------------")
        movie_hub.display_users()
        user_id = int(input("Please enter user ID: "))

        selected_user = movie_hub.users[user_id] # throws an index out of range error if user_id doesnt correspond to a user

    elif menu_choice == 3:
        print("---------------")
        movie_hub.search_movie()
        
    elif menu_choice == 4:
        print("---------------")
        movie_hub.display_movies()

    elif menu_choice == 5:
        print("---------------")
        movie_hub.display_highest_rated()

    elif menu_choice == 6:
        print("---------------")

        if selected_user is None:
            print("Please log in first.")

        selected_user.rate()

    elif menu_choice == 7:
        print("---------------")

        if selected_user is None:
            print("Please log in first.")

        selected_user.review()

    elif menu_choice == 8:
        print("---------------")

        if selected_user is None:
            print("Please log in first.")

        movie_hub.display_reviews(selected_user)

    elif menu_choice == 9:
        print("---------------")
        genre_list = []

        for i in range(len(movie_hub.films)):
            genre_list.append(movie_hub.films[i].genre)

        genre_list = list(set(genre_list))

        for i in range(len(genre_list)):
            print(f"{i} {genre_list[i]}")

        genre = input("\nPlease select a genre: ")
        movie_hub.filter_by_genre(genre_list[int(genre)])

    elif menu_choice == 10:
        break

    print("-----------------------------------------------")
