import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_world_news(category):
    # Specify the News API endpoint for top headlines
    endpoint = "https://newsapi.org/v2/top-headlines"

    # Set the parameters, including the API key and the category for world news
    params = {
        "apiKey": os.getenv('NEWS_API_KEY'),
        "category": category,  # You can change this to another category if needed
        "language": "en",       # Specify the language (English in this case)
        "country": "us"         # Specify the country (you can use 'us' for global news)
    }

    try:
        # Make the request to the News API
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the JSON response
        news_data = response.json()

        # Check if the request was successful
        if news_data['status'] == 'ok':
            # Extract the top 5 articles (excluding YouTube links)
            top_articles = news_data['articles'][:5]
            result_string = ""
            for i, article in enumerate(top_articles):
                result_string += f"{i+1}. Title: {article['title']}\n"
                result_string += f"   Source: {article['source']['name']}\n"
                result_string += f"   URL: {article['url']}\n"
                result_string += "-" * 30 + "\n"

            return result_string
        else:
            return f"Error: {news_data['message']}"

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"    
    
def newsAPI(category) -> str:
    """Useful to get news from the news API. Categories can be business, entertainment, general, health, science, sports, technology
    :param category : business, entertainment, general, health, science, sports or technology
    :return: news
    """
    ans = get_world_news(category)
    return ans