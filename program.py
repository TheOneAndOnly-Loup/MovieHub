class Database:
    def __init__(self):
        self.films = []
    def add_movie(self, movie_obj):
        self.films.append(movie_obj)
        # movie_obj.index = self.films.index(movie_obj)
    def remove_movie(self, movie_obj):
        self.films.remove(movie_obj)
    def display_movies(self):
        for i in range(len(self.films)):
            print(f"{i} {self.films[i]}\n")
    def search_movie(self):
        # write code here...
        pass

class Film:
    def __init__(self, name, age_rating, genre, year):
        self.name = name
        self.age_rating = age_rating
        self.genre = genre
        self.year = year
        self.reviews = [] # if no rating has been added, the movie will show 0/10... fix this later
        self.ratings = 0
        self.avg_rating = 0 # review later
    def __str__(self):
        return f"{self.name} ({self.year}) - {self.genre} - {self.age_rating} - {self.avg_rating}/10"

    # for reviews and ratings: add a way to assign a rating/review to a specific user
    def add_review(self, text): 
        self.reviews.append(text)
    
    def change_rating(self, value):
        self.avg_rating += value
        self.ratings += 1
        self.avg_rating = round(self.avg_rating / self.ratings, 2)  # average rating

class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.reviews = []
    def rate(self, movie_obj, value): # add user-review matching
        movie_obj.change_rating(value)
    def review(self, movie_obj, text): # here as well
        movie_obj.add_review(text)

movie_hub = Database()
starwars = Film("Star Wars: A New Hope", "PG", "Sci-Fi", 1977)
# godfather = Film("The Godfather", "R", "Crime", 1972)
# dark_knight = Film("The Dark Knight", "PG-13", "Action", 2008)
user1 = User("Joe", 1)
movie_hub.add_movie(starwars)
# user1.rate(starwars, 5)
# movie_hub.display_movies()

while True:
    print("""Welcome to MovieHub! What would you like to do?
    1. Search for a movie
    2. Display movies
    3. Rate movie
    4. Review movie\n""")

    menu_choice = int(input(": "))
    if menu_choice == 1:
        search = input("Search by name: ")
        for i in range(len(movie_hub.films)):
            try:
                if movie_hub.films[i].name == search:
                    movie_choice = movie_hub.films[i]
                    print("Movie found and selected")
            except ValueError:
                print("Movie not found!")
    
    elif menu_choice == 2:
        pass
    

    
    continue