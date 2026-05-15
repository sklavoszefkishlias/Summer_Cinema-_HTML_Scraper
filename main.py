import requests
import os
from bs4 import BeautifulSoup

# The URL of the page we want to scrape
URL = "https://www.athinorama.gr/cinema/guide/therinoi/cinemas/"

# A User-Agent makes your script look like a standard web browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15"
}

CACHE_FILE = "cached_page.html"

def get_html_content():
    # 1. Check if we already have the file saved locally
    if os.path.exists(CACHE_FILE):
        print("📁 Found cached HTML file. Loading from disk...")
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            return file.read()
            
    # 2. If the file doesn't exist, download it from the internet
    print("🌐 Cached file not found. Requesting from live website...")
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        
        # Save the downloaded HTML to our local file for next time
        with open(CACHE_FILE, "w", encoding="utf-8") as file:
            file.write(response.text)
            print(f"💾 Successfully saved webpage to '{CACHE_FILE}'")
            
        return response.text
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to retrieve the webpage: {e}")
        return None





def fetch_movie_data():
    try:
        # 1. Download the webpage
        response = get_html_content()

        # 2. Parse the HTML code
        soup = BeautifulSoup(response, "html.parser")

        # 3. Find all item containers on the page
        # (On a movie site, this might be div class="movie-card")
        items = soup.find_all("div", class_="item card-item")
        print(f"--- Found {len(items)} Items ---\n")
        print(type(items))

        for item in items:
            # Extract text and strip out extra whitespace
            cinema = item.find("h2", class_="item-title").text.strip()
            location = item.find("div", class_= "details").text.strip()

            movie_list = item.find_all("div", class_="item schedule-item")
            title_list = []
            for movie in movie_list:
                title_list.append(movie.find("h3").text.strip())

                

            ticket_prices = item.find("p", class_="summary").text.strip()

            '''price = item.find("h4", class_="price").text.strip()
            description = item.find("p", class_="description").text.strip()'''
            print(cinema)
            print(location)
            print(title_list)

            print(ticket_prices)

            '''# Print the results neatly
            print(f"📦 Cinema Name: {cinema}")
            print(f"💰 Price: {price}")
            print(f"📝 Info: {description}")
            print("-" * 40)'''
            

    except AttributeError:
        print("❌ Error: The website structure might have changed, or a class name is incorrect.")

if __name__ == "__main__":
    fetch_movie_data()