import argparse
from newsapi import NewsApiClient
import json
import time
from datetime import datetime, timedelta

api_key = json.load(open('data/secrets.json'))['API_KEY']
# Initialize API Client
newsapi = NewsApiClient(api_key=api_key)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Collect news articles about movies')
    parser.add_argument('movies', nargs='+', help='One or more movie titles to search for')
    parser.add_argument('--end-date', 
                       type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(),
                       default=datetime.now().date(),
                       help='End date for article search (YYYY-MM-DD). Defaults to today')
    args = parser.parse_args()
    
    # Calculate start date (1 month before end date)
    start_date = args.end_date - timedelta(days=7)
    
    return args.movies, start_date.strftime('%Y-%m-%d'), args.end_date.strftime('%Y-%m-%d')

# Replace hardcoded parameters with parsed arguments
movie_titles, start_date, end_date = parse_arguments()
page_size = 1  # Max articles per request
daily_request_limit = 50 # Limit based on API allowance
articles_per_movie = daily_request_limit // len(movie_titles)

# Function to fetch articles with rate limit considerations
def fetch_articles(movie_title, max_articles=250):
    articles = []
    page = 1
    requests_made = 0

    while len(articles) < max_articles and requests_made < articles_per_movie:
        response = newsapi.get_everything(
            q=movie_title,
            language='en',
            from_param=start_date,
            to=end_date,
            page_size=page_size,
            page=page,
            sort_by='publishedAt'
        )

        if 'articles' in response:
            articles.extend(response['articles'])
            page += 1
            requests_made += 1
            time.sleep(1)  # Wait to prevent hitting the rate limit
        else:
            break

    return articles[:max_articles]

def main():
    # Collect articles and save to JSON
    all_articles = {}
    for movie in movie_titles:
        articles = fetch_articles(movie)
        all_articles[movie] = articles
        print(f"Collected {len(articles)} articles for {movie}")

    # Save results to a JSON file
    with open("movie_articles.json", "w") as f:
        json.dump(all_articles, f)

    print("Data collection complete.")

if __name__ == '__main__':
    main()


# Use case: python src/collector.py "The Batman" 
#           python src/collector.py "The Batman" "Dune"
#           python src/collector.py "The Batman" --end-date 2024-11-10