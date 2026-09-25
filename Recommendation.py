movies = [
    {
        "title": "Avengers: Endgame",
        "genres": ["Action", "Adventure", "Sci-Fi"]
    },
    {
        "title": "Interstellar",
        "genres": ["Sci-Fi", "Adventure", "Drama"]
    },
    {
        "title": "Inception",
        "genres": ["Action", "Sci-Fi", "Thriller"]
    },
    {
        "title": "Titanic",
        "genres": ["Romance", "Drama"]
    },
    {
        "title": "The Dark Knight",
        "genres": ["Action", "Crime", "Drama"]
    },
    {
        "title": "Jurassic Park",
        "genres": ["Adventure", "Sci-Fi", "Thriller"]
    }
]


def get_user_preferences():
    print("------------------------------------------\nWelcome to the Movie Recommendation System!\n------------------------------------------")

    print("\nAvailable genres:")
    print("Action")
    print("Adventure")
    print("Sci-Fi")
    print("Drama")
    print("Thriller")
    print("Romance")
    print("Crime")

    user_input = input("\nEnter your favorite genres separated by commas: ")

    preferences = user_input.split(",")

    preferences = [
        genre.strip().title()
        for genre in preferences
    ]

    return preferences


def calculate_similarity(user_preferences, movie_genres):

    matching_genres = (
        set(user_preferences) & set(movie_genres)
    )

    score = len(matching_genres)

    percentage = (
        score / len(user_preferences)
    ) * 100

    return score, percentage


def recommend_movies(user_preferences):

    recommendations = []

    for movie in movies:

        score, percentage = calculate_similarity(
            user_preferences,
            movie["genres"]
        )

        recommendations.append({
            "title": movie["title"],
            "score": score,
            "percentage": percentage
        })

    recommendations.sort(
        key=lambda movie: movie["percentage"],
        reverse=True
    )

    return recommendations


def display_recommendations(recommendations):

    print("\nTop 3 Recommended Movies:")
    print("---------------------------")

    top_movies = [
        movie for movie in recommendations
        if movie["score"] > 0
    ][:3]

    if not top_movies:
        print("No matching movies found.")
        return

    for number, movie in enumerate(top_movies, start=1):

        print(
            number,
            ".",
            movie["title"],
            "-",
            round(movie["percentage"], 2),
            "% match"
        )

    print("\nRecommended Movies:")
    print("---------------------------")

    found = False

user_preferences = get_user_preferences()

recommendations = recommend_movies(user_preferences)

display_recommendations(recommendations)