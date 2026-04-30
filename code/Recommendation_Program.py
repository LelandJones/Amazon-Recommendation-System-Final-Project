import csv
import random

# ----------------------------
# Load movies from CSV
# ----------------------------
def load_movies(filename):
    movies = []
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie = {
                "title": row["Title"],
                "genres": row["Genres"].split("|")
            }
            movies.append(movie)
    return movies

# ----------------------------
# Get user reviews
# ----------------------------
def get_user_reviews(movies):
    print("\nRate the following movies (y = thumbs up, n = thumbs down):\n")
    
    sample_movies = random.sample(movies, 5)
    
    liked_genres = set()
    disliked_genres = set()
    
    for movie in sample_movies:
        while True:
            print(f"{movie['title']} ({', '.join(movie['genres'])})")
            rating = input("Did you like it? (y/n): ").lower()
            
            if rating == 'y':
                liked_genres.update(movie["genres"])
                break
            elif rating == 'n':
                disliked_genres.update(movie["genres"])
                break
            else:
                print("Please enter 'y' or 'n'.")
    
    return liked_genres, disliked_genres, sample_movies

# ----------------------------
# Recommend movies
# ----------------------------
def recommend_movies(movies, liked_genres, disliked_genres, already_seen):
    recommendations = []
    
    for movie in movies:
        if movie in already_seen:
            continue
        
        genres = set(movie["genres"])
        
        # Score movie based on overlap
        like_score = len(genres & liked_genres)
        dislike_score = len(genres & disliked_genres)
        
        score = like_score - dislike_score
        
        if score > 0:
            recommendations.append((movie, score))
    
    # Sort by best match
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    return recommendations[:5]

# ----------------------------
# Main program
# ----------------------------
def main():
    movies = load_movies("movies.csv")
    
    liked_genres, disliked_genres, seen_movies = get_user_reviews(movies)
    
    print("\n--- Recommendation Results ---\n")
    
    recommendations = recommend_movies(movies, liked_genres, disliked_genres, seen_movies)
    
    if not recommendations:
        print("No strong recommendations found. Try again!")
        return
    
    for movie, score in recommendations:
        print(f"{movie['title']} ({', '.join(movie['genres'])}) [Score: {score}]")

# Run program
if __name__ == "__main__":
    main()