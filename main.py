from neigbourhood_suggestion import search_by_input
from neighbourhood_reviews import get_neighbourhood_reviews

if __name__ == "__main__":
    search_by_input(input("Enter part of neighbourhood: "))
    get_neighbourhood_reviews(input("Enter full neighbourhood: "))
