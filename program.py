class Database:
    def __init__(self, films):
        self.films = films

class Film:
    def __init__(self, name, age_rating, genre, year):
        self.name = name
        self.age_rating = age_rating
        self.genre = genre
        self.year = year
        self.reviews = []
        self.avg_rating = 0 # review later
    def add_review(self, value, input): # Maybe seperate reviews and ratings
        self.reviews.append(input)
        self.avg_rating += value
        self.avg_rating = self.avg_rating / len(self.reviews) # average rating

class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.reviews = []